from card import Card

def mine_effect(player, game):
    treasures_in_hand = [card for card in player.hand if "Treasure" in card.card_type]
    if not treasures_in_hand:
        print("No Treasures in hand to trash.")
        return

    print(f"Your Treasures: {[card.name for card in treasures_in_hand]}")
    trash_choice = input("Choose a Treasure to trash: ").strip()
    to_trash = next((c for c in treasures_in_hand if c.name.lower() == trash_choice.lower()), None)

    if not to_trash:
        print("Invalid choice.")
        return

    player.hand.remove(to_trash)
    game.trash_pile.append(to_trash)
    max_cost = to_trash.cost + 3

    # Gainable Treasures from supply
    gainable = {name: pile for name, pile in game.supply.items()
                if pile and "Treasure" in pile[0].card_type and pile[0].cost <= max_cost}

    if not gainable:
        print("No available Treasure to gain.")
        return

    print(f"Available to gain (Treasure, cost ≤ {max_cost}): {', '.join(gainable.keys())}")
    gain_choice = input("Gain which Treasure? ").strip()

    if gain_choice in gainable and gainable[gain_choice]:
        gained = gainable[gain_choice].pop()
        player.hand.append(gained)
        print(f"{player.name} trashes {to_trash.name} and gains {gained.name} to hand.")
    else:
        print("Invalid gain choice.")

Mine = Card(
    "Mine",
    cost=5,
    card_type=["Action"],
    description="Trash a Treasure from your hand. Gain a Treasure to your hand costing up to +3 more.",
    effect=mine_effect,
    expansion="base"
)