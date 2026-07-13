from card import Card

def plat_effect(player, game):
    return 5  # +3 coin

Platinum = Card(
    "Platinum",
    cost=9,
    card_type = ['Treasure'],
    description="+5 Coins",
    effect=plat_effect,
    expansion = "prosperity"
)
