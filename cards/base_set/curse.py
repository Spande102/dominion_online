from card import Card

def curse_vp(player = None):
    return -1  # -1 VP

Curse = Card(
    "Curse",
    cost = 0,
    card_type = ['Curse'],
    description = "-1 VP",
    effect = None,
    expansion = "base"
)

Curse.get_victory_points = curse_vp
