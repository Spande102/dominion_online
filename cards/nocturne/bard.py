from card import Card

def bard_effect(player, game):
    # +$2
    player.coins += 2
    # Receive a Boon
    return f"+$2. {game.receive_boon(player)}"

Bard = Card(
    "Bard",
    cost=4,
    card_type=["Action", "Fate"],
    description="+$2. Receive a Boon.",
    effect=bard_effect,
    expansion="nocturne"
)
