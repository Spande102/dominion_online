from card import Card

def silk_road_vp(player):
    all_cards = player.deck + player.hand + player.discard_pile + player.in_play
    victory_cards = sum(1 for card in all_cards if "Victory" in card.card_type)
    return victory_cards // 4
Silk_Road = Card(
    "Silk Road",
    cost=4,
    card_type=["Victory"],
    description="Worth 1 VP for every 4 Victory cards in your deck (rounded down)",
    expansion="hinterlands_1st"
)
Silk_Road.get_victory_points = silk_road_vp