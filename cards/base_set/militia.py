from card import Card

def militia_discard_callback(player, game, selected_cards):
    """Callback for Militia discard interaction."""
    count = 0
    for card in selected_cards:
        if card in player.hand:
            player.hand.remove(card)
            player.discard_pile.append(card)
            count += 1
            
    print(f"{player.name} discarded {count} cards due to Militia.")

def militia_effect(player, game):
    # +2 Coins
    player.coins += 2
    print(f"{player.name} gets +2 Coins.")

    for other in game.players:
        if other is not player:
            if len(other.hand) > 3:
                num_to_discard = len(other.hand) - 3
                game.pending_interactions.append({
                    "player": other,
                    "type": "select_cards_from_hand",
                    "prompt": f"{other.name}: Militia - Discard {num_to_discard} cards.",
                    "min": num_to_discard,
                    "max": num_to_discard,
                    "callback": militia_discard_callback
                })
            else:
                print(f"{other.name} has 3 or fewer cards.")

Militia = Card(
    "Militia",
    cost = 4,
    card_type = ['Action', 'Attack'],
    description = "+2 Coins. Each other player discards down to 3 cards.",
    effect = militia_effect,
    expansion = "base"
)