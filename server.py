from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
from game import Game
from player import Player, InteractionRequired
from cards import load_cards
from utils.supply_build import add_standard_cards
from utils.kingdom_cards import choose_kingdom_cards

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Global game state (one game for now)
game_instance = None

# Global game state
game_instance = None
game_config = {
    'players': [],
     # Store config here until game starts
}

# Card Registry for lookups
CARD_REGISTRY = {}
def init_card_registry():
    all_cards, _ = load_cards()
    for card in all_cards:
        CARD_REGISTRY[card.name.lower()] = card

init_card_registry()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset')
def reset():
    global game_instance
    game_instance = None
    # Optional: Broadcast to others that game is reset, though they will find out on next interaction/poll
    socketio.emit('game_reset', {'message': "Game has been reset via hard reset."})
    return index() # Or redirect('/')

@socketio.on('connect')
def handle_connect():
    # If game exists, send state
    if game_instance:
        emit('game_state', game_instance.get_game_state())

@socketio.on('setup_game')
def handle_setup_game(data):
    try:
        global game_instance
        
        num_players = int(data.get('num_players', 2))
        kingdom_mode = data.get('kingdom_mode', 'random') 
        expansion_filter = data.get('expansions', []) # list of strings
        include_plat_col = data.get('include_platinum_colony', False)
        manual_cards = data.get('manual_kingdom_cards', []) # list of strings if mode is manual

        all_cards, cards_by_expansion = load_cards()
        
        # Create Players
        players = [Player(f"Player {i+1}") for i in range(num_players)]
        
        # Kingdom Setup
        selected_kingdom_cards = choose_kingdom_cards(
            cards_by_expansion, 
            interactive=False, 
            expansion_filter=expansion_filter if kingdom_mode == 'random' else None,
            specific_cards=manual_cards if kingdom_mode == 'manual' else None
        )
        
        supply = {card.name: [card for _ in range(10)] for card in selected_kingdom_cards}
        add_standard_cards(supply, len(players), include_colony=include_plat_col)
        
        game_instance = Game(players, supply)
        print(f"Game initialized with {num_players} players.")
        emit('game_start', {'message': "Game Started!"}, broadcast=True)
        emit('game_state', game_instance.get_game_state(), broadcast=True)
    except Exception as e:
        import traceback
        traceback.print_exc()
        emit('error', {'message': f"Failed to start game: {str(e)}"}, broadcast=True)

@socketio.on('play_card')
def handle_play_card(data):
    if not game_instance: return
    
    player_name = data.get('player_name')
    card_name = data.get('card_name')
    current = game_instance.current_player()
    
    if current.name != player_name:
        emit('error', {'message': "Not your turn!"})
        return

    # Check card type in hand to decide action vs treasure
    card_in_hand = next((c for c in current.hand if c.name == card_name), None)
    if not card_in_hand:
        emit('error', {'message': "Card not in hand!"})
        return

    if "Action" in card_in_hand.card_type:
        if game_instance.phase != 'action':
             emit('error', {'message': "Not in Action phase!"})
             return
        
        # Setup input state if provided (re-entrant call)
        input_data = data.get('input_data')
        if input_data:
            current.input_state = input_data

        try:
            success, msg = current.play_action_card(card_name, game_instance)
        except InteractionRequired as e:
            # Check for custom callback in payload
            custom_callback = e.payload.get('callback')
            
            if custom_callback:
                final_callback = custom_callback
            else:
                # Default resume logic for standard interactions
                def resume_callback(p, g, selected_cards):
                    # Convert card objects back to names for input_state compatibility
                    p.input_state = {"selection": [c.name for c in selected_cards]}
                    p.play_action_card(card_name, g)
                final_callback = resume_callback
                
            interaction_obj = {
                "player": current,
                "callback": final_callback
            }
            # Copy all other payload data (prompt, min, max, type, cards, etc.)
            for k, v in e.payload.items():
                if k != 'callback':
                    interaction_obj[k] = v
            
            game_instance.pending_interactions.append(interaction_obj)
            process_interaction_queue()
            return

    elif "Treasure" in card_in_hand.card_type:
        success, msg = current.play_treasure(card_name, game_instance)
        if success:
             game_instance.phase = 'buy' # Playing a treasure enters buy phase
    else:
        emit('error', {'message': "Cannot play this card manually."})
        return

    if success:
        emit('log', {'message': f"{player_name}: {msg}"}, broadcast=True)
        process_interaction_queue()
        emit('game_state', game_instance.get_game_state(), broadcast=True)
    else:
        emit('error', {'message': msg})

@socketio.on('play_treasures')
def handle_play_treasures(data):
    if not game_instance: return
    player_name = data.get('player_name')
    current = game_instance.current_player()
    
    if current.name != player_name:
         emit('error', {'message': "Not your turn!"})
         return
         
    count = current.play_all_treasures(game_instance)
    game_instance.phase = 'buy' # Auto advance to buy phase usually

    # Auto-end check
    if game_instance.check_auto_end_turn():
         emit('log', {'message': f"{player_name} has 0 buys, turn ended (or Night phase)."}, broadcast=True)
         if game_instance.is_game_over():
              broadcast_game_over(game_instance)
    
    emit('log', {'message': f"{player_name} played {count} treasures."}, broadcast=True)
    emit('game_state', game_instance.get_game_state(), broadcast=True)

@socketio.on('buy_card')
def handle_buy_card(data):
    if not game_instance: return
    
    player_name = data.get('player_name')
    card_name = data.get('card_name')
    current = game_instance.current_player()
    
    if current.name != player_name:
        emit('error', {'message': "Not your turn!"})
        return
        
    # Ensure they are in buy phase or have played treasures
    # For simplicity, we allow buying if they have buys
    
    success, msg = current.buy_card(card_name, game_instance)
    if success:
        emit('log', {'message': f"{player_name}: {msg}"}, broadcast=True)
        
        # Auto-end check
        if game_instance.check_auto_end_turn():
             emit('log', {'message': f"{player_name} has 0 buys, turn ended (or Night phase)."}, broadcast=True)
             if game_instance.is_game_over():
                 broadcast_game_over(game_instance)

        emit('game_state', game_instance.get_game_state(), broadcast=True)
    else:
        emit('error', {'message': msg})

@socketio.on('end_turn')
def handle_end_turn(data):
    if not game_instance: return
    player_name = data.get('player_name')
    current = game_instance.current_player()
    
    if current.name != player_name:
        emit('error', {'message': "Not your turn!"})
        return
        
    game_instance.next_turn()
    
    if game_instance.is_game_over():
        broadcast_game_over(game_instance)

    emit('log', {'message': f"{player_name} ended turn."}, broadcast=True)
    emit('game_state', game_instance.get_game_state(), broadcast=True)

def broadcast_game_over(game):
    """Formats final scores and broadcasts them to chat/log."""
    if not game.final_scores:
        game.tally_scores() # Ensure tallied
        
    scores = game.final_scores
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    msg = "GAME OVER! Final Scores: " + ", ".join([f"{p}: {s} VP" for p, s in sorted_scores])
    emit('chat_log', {'player': 'System', 'message': msg}, broadcast=True)
    emit('log', {'message': msg}, broadcast=True)

@socketio.on('chat_message')
def handle_chat(data):
    player_name = data.get('player_name')
    message = data.get('message', '').strip()
    
    # Broadcast the original message first
    emit('chat_log', {'player': player_name, 'message': message}, broadcast=True)

    # Command Handling
    if message.startswith('!'):
        parts = message.split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        response = None
        
        if command == '!help':
            response = "Commands: !coins, !actions, !description <card_name> (or !desc)"
            
        elif command == '!coins':
            if game_instance:
                p = next((p for p in game_instance.players if p.name == player_name), None)
                if p:
                    response = f"You have {p.coins} coins."
                else:
                    response = "Player not found."
            else:
                response = "Game not running."

        elif command == '!actions':
            if game_instance:
                p = next((p for p in game_instance.players if p.name == player_name), None)
                if p:
                    response = f"You have {p.actions} actions."
                else:
                    response = "Player not found."
            else:
                 response = "Game not running."
                 
        elif command == '!description' or command == '!desc':
            args = args.strip()
            if not args:
                response = "Usage: !description <card_name>"
            else:
                 card = CARD_REGISTRY.get(args.lower())
                 if card:
                     response = f"{card.name}: {card.description}"
                 else:
                     response = f"Card '{args}' not found."

        if response:
            emit('chat_log', {'player': 'System', 'message': response}, broadcast=True)

@socketio.on('resign')
def handle_resign(data):
    player_name = data.get('player_name')
    emit('log', {'message': f"PLAYER RESIGNED: {player_name} has resigned. The game is over."}, broadcast=True)
    
    # Reset game
    global game_instance
    game_instance = None
    
    # Notify clients to reset/show game over
    emit('game_over_resignation', {'player_name': player_name}, broadcast=True)

@socketio.on('submit_interaction')
def handle_interaction_response(data):
    if not game_instance: return
    
    player_name = data.get('player_name')
    # selection is list of card names
    selection = data.get('selection', []) 
    
    if not game_instance.pending_interactions:
        emit('error', {'message': "No interaction pending."})
        return

    interaction = game_instance.pending_interactions[0]
    target_player = interaction['player']
    
    if target_player.name != player_name:
        emit('error', {'message': "Not your interaction!"})
        return
        
    # Process selection
    selected_cards = []
    
    
    if interaction.get('type') == 'select_from_supply':
        # Map names to supply cards (peek)
        for name in selection:
             if name in game_instance.supply and game_instance.supply[name]:
                 selected_cards.append(game_instance.supply[name][0])
    elif interaction.get('type') == 'sentry_resolution':
        # Pass raw selection (dict of trash/discard/top_deck) directly to callback
        selected_cards = selection
    else:
        # Default: Map names to cards in hand
        # We work on a copy to handle duplicates correctly if hand has multiple coppers
        hand_copy = list(target_player.hand)
        
        for name in selection:
            found = next((c for c in hand_copy if c.name == name), None)
            if found:
                selected_cards.append(found)
                hand_copy.remove(found)
            else:
                pass
            
    # Execute callback
    try:
        if 'callback' in interaction:
            interaction['callback'](target_player, game_instance, selected_cards)
        
        # Remove completed interaction
        game_instance.pending_interactions.pop(0)
        
        # Log completion
        emit('log', {'message': f"{player_name} completed interaction."}, broadcast=True)
        
        # Check for next interaction
        process_interaction_queue()
        
        # Update state
        emit('game_state', game_instance.get_game_state(), broadcast=True)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        emit('error', {'message': str(e)})

def process_interaction_queue():
    if not game_instance or not game_instance.pending_interactions:
        return

    interaction = game_instance.pending_interactions[0]
    target_player = interaction['player']
    
    
    # Base payload
    payload = {
        "player_name": target_player.name,
    }
    
    # Merge interaction details, excluding server-only objects
    for k, v in interaction.items():
        if k not in ['player', 'callback']:
             payload[k] = v
             
    # Ensure defaults if missing
    if 'prompt' not in payload: payload['prompt'] = "Action required"
    if 'type' not in payload: payload['type'] = 'select'
    
    # Broadcast request so everyone knows X is thinking (frontend filters by name)
    emit('interaction_request', payload, broadcast=True)

@socketio.on('reset_game')
def handle_reset_game(data):
    """Resets the game state to None, effectively sending everyone to lobby."""
    global game_instance
    game_instance = None
    emit('game_reset', {'message': "Game has been reset."}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
