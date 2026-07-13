from card import Card

def chancellor_effect(player, game):
    player.coins += 2

    discard = input("Discard your entire deck? (y/n): ").strip().lower() == 'y'
    if discard:
        player.discard_pile.extend(player.deck)
        player.deck.clear()
        print(f"{player.name} discards their deck.")
    else:
        print("chose not to discard")


Chancellor = Card(
    "Chancellor",
    cost=3,
    card_type = ['Action'],
    description="+2 Coins. You may immediately put your deck into your discard pile.",
    effect=chancellor_effect,
    expansion = "base_1st_edition"
)