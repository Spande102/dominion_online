from card import Card

def grand_market_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    player.buys += 1
    player.coins += 2

GrandMarket = Card(
    "Grand Market",
    cost=6,
    card_type=["Action"],
    description="+1 Card, +1 Action, +1 Buy, +2 Coins. Cannot be bought if you have Copper in play.",
    effect=grand_market_effect,
    expansion="prosperity"
)

def grand_market_can_buy(player, game):
    if any(c.name == "Copper" for c in player.in_play):
        return False, "Cannot buy Grand Market while Copper is in play."
    return True, ""

GrandMarket.can_buy = grand_market_can_buy