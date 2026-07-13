from card import Card

def spy_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    for target_player in game.players:
        # Reveal the top card of the target player's deck
        revealed_card = target_player.draw_cards(1, return_card=True)
        if revealed_card:
            print(f"{target_player.name} revealed {revealed_card.name}.")

            # Ask the player playing Spy what to do with the revealed card
            while True:
                choice = input(
                    f"Do you want to discard {target_player.name}'s revealed card "
                    f"({revealed_card.name})? (yes/no): "
                ).strip().lower()
                if choice == "yes":
                    # Discard the revealed card
                    target_player.discard_pile.append(revealed_card)
                    print(f"{target_player.name}'s card was discarded.")
                    break
                elif choice == "no":
                    # Put the card back on the top of the deck
                    target_player.deck.append(revealed_card)
                    print(f"{target_player.name}'s card remains on top of their deck.")
                    break
                else:
                    print("Invalid choice. Please type 'yes' or 'no'.")


Spy = Card(
    "Spy",
    cost=4,
    card_type=['Action', 'Attack'],
    description="+1 Card +1 Action. Each player (including you) reveals the top card of their deck and either discards it or puts it back, your choice.",
    effect=None,
    expansion = "base_1st_edition"
)