from card import Card

def silver_effect(player, game):
    return 2  # +2 coin

Silver = Card(
    "Silver",
    cost = 3,
    card_type = ['Treasure'],
    description = "+2 Coins",
    effect = silver_effect,
    expansion = "base"
)
