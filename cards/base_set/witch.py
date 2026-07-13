from card import Card

def witch_effect(player, game):
    # +2 Cards
    player.draw_cards(2)

    # Each other player gains a Curse (if available)
    for other in game.players:
        if other is not player:
            if "Curse" in game.supply and game.supply["Curse"]:
                curse_card = game.supply["Curse"].pop()
                other.discard_pile.append(curse_card)
                print(f"{other.name} gains a Curse.")
            else:
                print("No Curse cards left in supply.")

Witch = Card(
    name = "Witch",
    cost = 5,
    card_type = ['Action', 'Attack'],
    description = "+2 Cards; each other player gains a Curse.",
    effect = witch_effect,
    expansion = "base"
)