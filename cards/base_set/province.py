from card import Card

def province_vp(player = None):
    return 6  # +6 VP

Province = Card(
    "Province",
    cost = 8,
    card_type = ['Victory'],
    description = "+6 VP",
    effect = None,
    expansion = "base"
)

Province.get_victory_points = province_vp

