from card import Card

def village_effect(player, game):
    player.draw_cards(1)
    player.actions += 2

Village = Card(
    "Village",
    cost = 3,
    card_type = ['Action'],
    description = "+1 Card, +2 Actions",
    effect = village_effect,
    expansion = "base"
)
