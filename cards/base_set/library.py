from card import Card

def library_effect(player, game):

    set_aside = []
    while len(player.hand) < 7:
        card = player.draw_cards(1, return_card=True)
        if not card:
            break
        if "Action" in card.card_type:
            keep = input(f"Drawn {card.name} (Action). Keep? (y/n): ").strip().lower() == 'y'
            if keep:
                player.hand.append(card)
            else:
                set_aside.append(card)
        else:
            player.hand.append(card)
    player.discard_pile.extend(set_aside)


Library = Card(
    "Library",
    cost = 5,
    card_type = ['Action'],
    description = "Draw until you have 7 cards in hand, skipping any Action cards you choose to; set those aside, discarding them afterwards.",
    effect = library_effect,
    expansion = "base"
)