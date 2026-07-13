from game import Game
from player import Player
from cards import load_cards
from utils.supply_build import add_standard_cards
from utils.kingdom_cards import choose_kingdom_cards
import json

def test_game_flow():
    print("Initializing Game...")
    all_cards, cards_by_expansion = load_cards()
    players = [Player("Player 1"), Player("Player 2")]
    selected_kingdom_cards = choose_kingdom_cards(cards_by_expansion, interactive=False)
    supply = {card.name: [card for _ in range(10)] for card in selected_kingdom_cards}
    add_standard_cards(supply, len(players), include_colony=False)
    
    game = Game(players, supply)
    print("Game Initialized.")
    
    # Check Initial State
    state = game.get_game_state()
    print("Initial State Keys:", state.keys())
    assert state['current_player'] == "Player 1"
    assert len(state['players']) == 2
    assert state['players'][0]['name'] == "Player 1"
    
    # Simulate Player 1 Turn
    p1 = game.current_player()
    print(f"Current Player: {p1.name}")
    
    # Play Treasures
    print("Playing Treasures...")
    coins_before = p1.coins
    count = p1.play_all_treasures(game)
    print(f"Played {count} treasures. Coins: {p1.coins}")
    
    # Buy a Copper (should always be there)
    print("Buying Copper...")
    if 'Copper' in game.supply and game.supply['Copper']:
        success, msg = p1.buy_card('Copper', game)
        print(f"Buy Result: {success} - {msg}")
    
    # End Turn
    print("Ending Turn...")
    game.next_turn()
    
    # Verify it's Player 2's turn
    state = game.get_game_state()
    assert state['current_player'] == "Player 2"
    print("Turn passed to Player 2 successfully.")

if __name__ == "__main__":
    try:
        test_game_flow()
        print("Verification Passed!")
    except Exception as e:
        print(f"Verification Failed: {e}")
        import traceback
        traceback.print_exc()
