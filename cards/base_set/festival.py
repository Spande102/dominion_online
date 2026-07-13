from card import Card

def festival_effect(player, game):
    player.actions += 2
    player.buys += 1
    player.coins += 2

Festival = Card(
    "Festival",
    cost = 5,
    card_type = ['Action'],
    description = "+2 Actions, +1 Buy, +2 Coins",
    effect = festival_effect,
    expansion = "base"
)
