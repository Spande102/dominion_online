from card import Card

def duke_vp(player):
    duchy_count = sum(1 for card in (player.deck + player.hand + player.discard_pile)
                      if card.name == "Duchy")
    return duchy_count

Duke = Card(
    "Duke",
    cost = 5,
    card_type = "Victory",
    description = "Worth 1 VP per Duchy you have",
    expansion = "intrigue"
)
Duke.get_victory_points = duke_vp