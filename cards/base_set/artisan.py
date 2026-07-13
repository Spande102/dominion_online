from card import Card

def artisan_effect(player, game):

    #Gaining card
    max_cost = 5
    gainable = {name: pile for name, pile in game.supply.items() if pile and pile[0].cost <= max_cost}

    if not gainable:
        print("No available cards to gain.")
        return

    print(f"Available to gain (cost ≤ {max_cost}): {', '.join(sorted(gainable.keys()))}")

    while True:
        gain_choice = input("Gain which card? ").strip()
        if gain_choice in gainable and gainable[gain_choice]:
            gained_card = gainable[gain_choice].pop()
            player.hand.append(gained_card)
            print(f"{player.name} gains {gained_card.name} to their hand.")
            break
        else:
            print("Invalid choice. Please choose a valid card.")

    # Topdecking
    while True:
        print(f"\nYour hand: {[card.name for card in player.hand]}")
        choice = input("Choose a card from your hand to put onto your deck: ").strip()
        card_to_topdeck = next((c for c in player.hand if c.name.lower() == choice.lower()), None)

        if card_to_topdeck:
            player.hand.remove(card_to_topdeck)
            player.deck.insert(0, card_to_topdeck)
            print(f"{player.name} topdecks {card_to_topdeck.name}.")
            break
        else:
            print("Invalid choice. Please choose a card from your hand.")

Artisan = Card(
    "Artisan",
    cost=6,
    card_type=["Action"],
    description="Gain a card to your hand costing up to 5. Put a card from your hand onto your deck.",
    effect=artisan_effect,
    expansion="base"
)