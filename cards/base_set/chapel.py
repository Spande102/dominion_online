from card import Card

def chapel_effect(player, game):
    # Show hand
    print(f"\nYour hand: {[card.name for card in player.hand]}")

    cards_trashed = 0
    while cards_trashed < 4 and player.hand:
        choice = input(f"Choose a card to trash (or press Enter to finish): ").strip()

        if not choice:  # Player finishes trashing
            break

        # Find the chosen card
        card_to_trash = next((c for c in player.hand if c.name.lower() == choice.lower()), None)
        if not card_to_trash:
            print("Invalid card. Please choose a valid card from your hand.")
            continue

        # Remove a card from hand and increment counter
        player.hand.remove(card_to_trash)
        cards_trashed += 1
        print(f"{player.name} trashes {card_to_trash.name}.")
        print(f"\nYour hand: {[card.name for card in player.hand]}")

    print(f"{player.name} has trashed {cards_trashed} card(s).")

Chapel = Card(
    "Chapel",
    cost=2,
    card_type=['Action'],
    description="Trash up to 4 cards from your hand.",
    effect=chapel_effect,
    expansion="base"
)
