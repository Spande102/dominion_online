from card import Card

def estate_vp(player=None):
    return 1

Estate = Card(
    "Estate",
    cost=2,
    card_type = ['Victory'],
    description="1 VP",
    effect=None,
    expansion="base"
)
Estate.get_victory_points = estate_vp
