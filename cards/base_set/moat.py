from card import Card

def moat_effect(player, game):
    player.draw_cards(2)

def moat_reaction(player, attack_card_name):
    return True  # Always blocks

Moat = Card(
    "Moat",
    cost = 2,
    card_type = ['Action', 'Reaction'],
    description = "+2 Cards | When another player plays an Attack card, you may first reveal this from your hand, to be unaffected by it.",
    effect = moat_effect,
    expansion = "base"
)