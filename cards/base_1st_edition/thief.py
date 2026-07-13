from card import Card

def thief_effect(player, game):
    for other in game.other_players(player):
        # Reveal the top 2 cards of the other player's deck
        revealed = other.draw_cards(2, return_card=True)
        print(f"{other.name} revealed: {[card.name for card in revealed]}")

        # Filter revealed cards for Treasures
        treasures = [card for card in revealed if "Treasure" in card.card_type]
        non_treasures = [card for card in revealed if card not in treasures]

        # Handle Treasures
        for treasure in treasures:
            # Choose Treasure to trash (assuming valid input handling exists)
            to_trash = player.choose_card_from([treasure], f"Trash {other.name}'s Treasure card ({treasure.name})?")
            if to_trash:
                other.trash_card(to_trash)
                print(f"{to_trash.name} from {other.name}'s deck is trashed.")

                # Offer the player the chance to gain the trashed card
                gain = input(f"Do you want to gain {to_trash.name}? (y/n): ").strip().lower()
                if gain == 'y':
                    player.discard_pile.append(to_trash)
                    print(f"{player.name} gains {to_trash.name}.")

        # Discard non-Treasure cards
        other.discard_pile.extend(non_treasures + [card for card in treasures if card not in [to_trash]])
        print(f"{other.name} discards: {[card.name for card in non_treasures]} + remaining cards.")


Thief = Card(
    "Thief",
    cost=4,
    card_type = ['Action','Attack'],
    description="Each other player reveals the top 2 cards of their deck. If they revealed any Treasure cards, they trash one of them that you choose. You may gain any or all of these trashed cards. They discard the other revealed cards.",
    effect=thief_effect,
    expansion = "base_1st_edition"
)