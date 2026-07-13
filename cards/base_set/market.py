from card import Card


def market_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    player.buys += 1
    player.coins += 1

Market = Card(
    "Market",
    cost = 5,
    card_type = ['Action'],
    description = "+1 Card, +1 Action, +1 Buy, +1 Coin",
    effect = market_effect,
    expansion = "base"
)
