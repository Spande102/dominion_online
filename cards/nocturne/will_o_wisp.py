from card import Card

def will_o_wisp_effect(player, game):
    # +1 Card, +1 Action
    player.draw_cards(1)
    player.actions += 1
    
    # Reveal top card of deck. If it costs $2 or less, put it into hand.
    # Logic:
    top_card = player.draw_cards(1, return_card=True)
    if top_card:
        # Check cost
        if top_card.cost <= 2:
            print(f"Will-o'-Wisp: Revealed {top_card.name} ($2 or less), putting into hand.")
            player.hand.append(top_card)
            return "+1 Card, +1 Action. Revealed card added to hand."
        else:
            print(f"Will-o'-Wisp: Revealed {top_card.name} (>$2), putting back.")
            player.deck.append(top_card) # Put back
            return "+1 Card, +1 Action. Revealed card returned to deck."
    return "+1 Card, +1 Action."

WillOWisp = Card(
    "Will-o'-Wisp",
    cost=0,
    card_type=["Action", "Spirit"],
    description="+1 Card, +1 Action. Reveal the top card of your deck. If it costs $2 or less, put it into your hand. (This card is not in the Supply)",
    effect=will_o_wisp_effect,
    expansion="nocturne"
)
