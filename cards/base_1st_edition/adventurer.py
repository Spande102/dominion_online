from card import Card


def adventurer_effect(player, game):
    treasures = 0
    revealed = []
    while treasures < 2:
        card = player.draw(1, return_card=True)
        if not card:
            break
        if "Treasure" in card.card_type:
            player.hand.append(card)
            treasures += 1
        else:
            revealed.append(card)
    player.discard_pile.extend(revealed)

Adventurer = Card(
    "Adventurer",
    cost=6,
    card_type=['Action'],
    description="Reveal cards from your deck until you reveal 2 Treasure cards. Put those Treasure cards into your hand and discard the other revealed cards.",
    effect=adventurer_effect,
    expansion = "base_1st_edition"
)