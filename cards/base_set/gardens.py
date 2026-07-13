from card import Card

def gardens_vp(player):
    total_cards = len(player.deck) + len(player.hand) + len(player.discard_pile) + len(player.in_play)
    return total_cards // 10

Gardens = Card(
    "Gardens",
    cost=4,
    card_type=["Victory"],
    description="Worth 1 VP for every 10 cards in your deck (rounded down)",
    expansion="base"
)
Gardens.get_victory_points = gardens_vp