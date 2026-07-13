from card import Card


def remodel_effect(player, game):
    # Show hand
    print(f"\nYour hand: {[card.name for card in player.hand]}")
    # choice = input("Choose a card to trash: ").strip()
    choice = None # Interactive choice not supported yet

    # Find chosen card
    card_to_trash = next((c for c in player.hand if c.name.lower() == choice.lower()), None)
    if not card_to_trash:
        print("Invalid card.")
        return

    player.hand.remove(card_to_trash)
    print(f"{player.name} trashes {card_to_trash.name}.")

    # Choose gainable cards
    max_cost = card_to_trash.cost + 2
    gainable = {name: pile for name, pile in game.supply.items() if pile and pile[0].cost <= max_cost}
    print(f"Available to gain (cost ≤ {max_cost}): {', '.join(gainable.keys())}")

    # gain_choice = input("Gain which card? ").strip()
    gain_choice = None
    if gain_choice in gainable and gainable[gain_choice]:
        gained_card = gainable[gain_choice].pop()
        player.discard_pile.append(gained_card)
        print(f"{player.name} gains {gained_card.name}.")
    else:
        print("Invalid gain choice.")


Remodel = Card(
    "Remodel",
    cost = 4,
    card_type = ['Action'],
    description = "Trash a card from your hand. Gain a card costing up to 2 more.",
    effect = remodel_effect,
    expansion = "base"
)