from card import Card

def bandit_effect(player, game):
    # Gain a Gold
    if "Gold" in game.supply and game.supply["Gold"]:
        gold = game.supply["Gold"].pop()
        player.discard_pile.append(gold)
        print(f"{player.name} gains a Gold.")
    else:
        print("No Golds left to gain.")

    # Attack other players
    for other_player in game.players:
        if other_player == player:
            continue

        # Reveal top 2 cards
        revealed = [other_player.draw_card() for _ in range(2)]
        revealed = [card for card in revealed if card is not None]
        print(f"{other_player.name} reveals: {[card.name for card in revealed]}")

        # Find non-Copper Treasures
        treasures = [card for card in revealed if "Treasure" in card.card_type and card.name != "Copper"]
        if treasures:
            # Trash one - highest cost(shouldnt do this but i didnt code the player's choice)
            to_trash = sorted(treasures, key=lambda c: c.cost, reverse=True)[0]
            revealed.remove(to_trash)
            game.trash_pile.append(to_trash)
            print(f"{other_player.name} trashes {to_trash.name}.")

        # Discard the rest
        for card in revealed:
            other_player.discard_pile.append(card)
            print(f"{other_player.name} discards {card.name}.")

Bandit = Card(
    "Bandit",
    cost=5,
    card_type=["Action", "Attack"],
    description="Gain a Gold. Each other player reveals the top 2 cards of their deck, trashes a non-Copper Treasure among them, and discards the rest.",
    effect=bandit_effect,
    expansion="base"
)