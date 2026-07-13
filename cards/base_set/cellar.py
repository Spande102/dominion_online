from card import Card

def cellar_effect(player, game):

    player.actions += 1
    discards = player.choose_multiple_from_hand(prompt="Choose cards to discard:")

    for card in discards:
        player.hand.remove(card)
        player.discard_pile.append(card)
    player.draw_cards(len(discards))

    print(f"{player.name} discards {len(discards)} cards and draws {len(discards)} cards.")

Cellar = Card(
    "Cellar",
    cost=2,
    card_type=['Action'],
    description="+1 Action Discard any number of cards. +1 Card per card discarded.",
    effect=cellar_effect,
    expansion="base"
)