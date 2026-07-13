from card import Card

def bazaar_effect(player, game):
    player.draw_cards(1)
    player.actions +=2
    player.coins +=1

Bazaar = Card(
    "Bazaar",
    cost=5,
    card_type = ['Action'],
    description="+1 Card, +2 Actions, +1 Coin",
    effect=bazaar_effect,
    expansion = "seaside"
)

