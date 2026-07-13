from card import Card

def duchy_vp(player = None):
    return 3  # +3 VP

Duchy = Card(
    "Duchy",
    cost = 5,
    card_type = ['Victory'],
    description = "+3 VP",
    effect = None,
    expansion = "base"
)

Duchy.get_victory_points = duchy_vp