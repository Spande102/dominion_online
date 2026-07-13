from card import Card

def colony_vp(player = None):
    return 10  # +10 VP

Colony = Card(
    "Colony",
    cost = 11,
    card_type = ['Victory'],
    description = "+10 VP",
    effect = None,
    expansion = "prosperity"
)

Colony.get_victory_points = colony_vp
