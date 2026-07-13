from card import Card

def vassal_effect(player, game):
    player.coins += 2
    top = player.draw_cards(1, return_card=True)
    if top:
        print(f"Discarded {top.name}.")
        player.discard_pile.append(top)
        if "Action" in top.card_type:
            play_it = input(f"Play {top.name}? (y/n): ").strip().lower() == 'y'
            if play_it:
                player.discard_pile.remove(top)
                top.effect(player, game)

Vassal = Card(
    "Vassal",
    cost=3,
    card_type=["Action"],
    description="You may play an Action card from your hand twice.",
    effect=vassal_effect,
    expansion="base",
)