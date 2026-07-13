from card import Card

def bureaucrat_effect(player, game):
    silver = game.topdeck_gained_card(player, "Silver")
    if silver:
        print(f"{player.name} gains a Silver onto their deck.")
    else:
        print("No Silver available in the supply!")
        return

    for other in game.other_players(player):
        victory_cards = [c for c in other.hand if "Victory" in c.card_type]
        if victory_cards:
            chosen = player.choose_card_from(victory_cards, prompt=f"{other.name}, choose a Victory card to topdeck:")
            other.hand.remove(chosen)
            other.deck.append(chosen)
            print(f"{other.name} topdecks {chosen.name}.")
        else:
            print(f"{other.name} reveals {other.hand}.")

Beureaucrat = Card(
    "Beureaucrat",
    cost=4,
    card_type=['Action', 'Attack'],
    description="Gain a Silver onto your deck. Each other player reveals a Victory card from their hand and puts it onto their deck (or reveals a hand with no Victory cards).",
    effect=bureaucrat_effect,
    expansion="base"
)

