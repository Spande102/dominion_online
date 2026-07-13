from card import Card

def woodcutter_effect(player, game):
    player.buys +=1
    player.coins +=2

Woodcutter = Card(
    "Woodcutter",
    cost=3,
    card_type = ['Action'],
    description="+1 Buy, +2 Coins",
    effect=woodcutter_effect,
    expansion = "base_1st_edition"
)

