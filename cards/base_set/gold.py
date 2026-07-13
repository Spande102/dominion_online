from card import Card

def gold_effect(player, game):
    return 3  # +3 coin

Gold = Card(
    "Gold",
    cost=6,
    card_type = ['Treasure'],
    description="+3 Coins",
    effect=gold_effect,
    expansion = "base"
)

