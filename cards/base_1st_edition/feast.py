from card import Card


def feast_effect(player, game):
    max_cost = 5
    gainable = {name: pile for name, pile in game.supply.items() if pile and pile[0].cost <= max_cost}
    choice = input(f"Gain card (≤ 5): ").strip()
    if choice in gainable:
        gained = gainable[choice].pop()
        player.discard_pile.append(gained)
        print(f"{player.name} gains {gained.name}.")
    player.trash_card("Feast", game, zone="in_play")

Feast = Card(
    "Feast",
    cost=4,
    card_type=['Action'],
    description="Trash this card. Gain a card costing up to 5",
    effect=feast_effect,
    expansion="base_1st_edition"
)