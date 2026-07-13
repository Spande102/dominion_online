from card import Card

def council_room_effect(player, game):
    player.draw_cards(4)
    player.buys += 1
    for other_player in game.players:
        if other_player != player:
            other_player.draw_cards(1)


Council_Room = Card(
    "Council Room",
    cost=5,
    card_type=["Action"],
    description="+4 Cards +1 Buy. Each other player draws a card.",
    effect=council_room_effect,
    expansion="base"
)