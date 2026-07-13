from card import Card

def lab_effect(player, game):
    player.draw_cards(2)
    player.actions += 1

Laboratory = Card(
    "Laboratory",
    cost=5,
    card_type = ['Action'],
    description="+2 Cards, +1 Actions",
    effect=lab_effect,
    expansion = "base"
)
