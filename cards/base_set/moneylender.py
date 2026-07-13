from card import Card

def moneylender_effect(player, game):

    copper_in_hand = next((card for card in player.hand if card.name == "Copper"), None)
    if copper_in_hand:
        # Auto-trash for now since web UI doesn't support interactive choices in mid-effect yet
        player.hand.remove(copper_in_hand)
        game.trash_pile.append(copper_in_hand)
        player.coins += 3
        # Use return value to bubble up msg if needed, but print works for server logs redirection? 
        # No, prints go to stdout. We need to rely on the side-effects.
        # The Player.play_action_card only returns a generic success msg. 
        # We might want to enhance the return msg if we could.
    else:
        pass # No copper, nothing happens

Moneylender = Card(
    "Moneylender",
    cost=4,
    card_type=["Action"],
    description="You may trash a Copper from your hand. If you do, +3 Coins.",
    effect=moneylender_effect,
    expansion="base"
)