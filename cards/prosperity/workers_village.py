from card import Card

def workers_village_effect(player, game):
    player.draw_cards(1)
    player.actions += 2
    player.buys += 1


Workers_Village = Card(
    "Worker's Village",
    cost=4,
    card_type = ['Action'],
    description="+1 Card, +2 Actions, +1 Buy",
    effect=workers_village_effect,
    expansion = "prosperity"
)


