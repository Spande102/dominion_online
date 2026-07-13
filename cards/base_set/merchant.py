from card import Card

def merchant_effect(player, game):

    player.draw_cards(1)
    player.actions += 1
    player.merchant_triggered = False  # Reset flag for this turn
    print(f"{player.name} draws a card and gets +1 Action.")

Merchant = Card(
    "Merchant",
    cost=3,
    card_type=["Action"],
    description="+1 Card, +1 Action. The first time you play a Silver this turn, +1 Coin.",
    effect=merchant_effect,
    expansion="base"
)