from card import Card

def throne_room_effect(player, game):

    action_cards = [c for c in player.hand if "Action" in c.card_type]
    if not action_cards:
        print("No Action cards to Throne Room.")
        return
    chosen = player.choose_card_from(action_cards, "Choose Action to play twice:")
    player.hand.remove(chosen)
    print(f"{player.name} plays {chosen.name} twice.")
    chosen.effect(player, game)
    chosen.effect(player, game)

Throne_room = Card(
    "Throne Room",
    cost=4,
    card_type=["Action"],
    description="You may play an Action card from your hand twice.",
    effect=throne_room_effect,
    expansion="base",
)