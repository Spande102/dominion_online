from card import Card

def smithy_effect(player, game):
    player.draw_cards(3)
    print(f"{player.name} draws 3 cards.")

Smithy = Card(
    "Smithy",
    cost = 4,
    card_type = ['Action'],
    description = "+3 Cards",
    effect = smithy_effect,
    expansion = "base"
)
