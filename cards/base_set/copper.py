from card import Card

def copper_effect(player, game):
    return 1  # +1 coin

Copper = Card(
    "Copper",
    cost=0,
    card_type = ['Treasure'],
    description="+1 Coin",
    effect=copper_effect,
    expansion = "base"
)
