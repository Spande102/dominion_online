from card import Card

def monument_effect(player, game):
    player.coins += 2
    player.victory_tokens += 1


Monument = Card(
    "Monument",
    cost=5,
    card_type = ['Action','Attack'],
    description="+2 Coins, +1 Victory Token",
    effect=monument_effect,
    expansion = "prosperity"
)