from card import Card

def harbinger_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    if player.discard_pile:
        choice = player.choose_from_list(player.discard_pile, "Choose a card from discard to topdeck (or skip):")
        if choice:
            player.discard_pile.remove(choice)
            player.deck.append(choice)
            print(f"{player.name} topdecks {choice.name}.")

Harbinger = Card(
    "Harbinger",
    cost=3,
    card_type=["Action"],
    description="+1 Card +1 Action. Look through your discard pile. You may put a card from it onto your deck.",
    effect=harbinger_effect,
    expansion="base"
)