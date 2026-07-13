from player import Player
from game import Game
from cards import load_cards  # Updated __init__.py now returns cards
from utils.supply_build import add_standard_cards
from utils.kingdom_cards  import choose_kingdom_cards

def main():
    # Load all available cards
    all_cards, cards_by_expansion = load_cards()

    # Prompt for player count
    while True:
        try:
            num_players = int(input("How many players? (2–4): "))
            if 2 <= num_players <= 4:
                break
            else:
                print("Dominion is best with 2–4 players.")
        except ValueError:
            print("Enter a valid number.")

    players = [Player(input(f"Enter name for Player {i+1}: ")) for i in range(num_players)]

    # Choose 10 Kingdom cards (either manually or randomly)
    selected_kingdom_cards = choose_kingdom_cards(cards_by_expansion)
    if len(selected_kingdom_cards) != 10:
        print("Invalid kingdom card setup. Exiting.")
        return

    # Create full supply: start with Kingdom cards
    supply = {card.name: [card for _ in range(10)] for card in selected_kingdom_cards}

    # Add base cards like Copper, Silver, Gold, Estates, Duchies, Provinces, Curses

    add_standard_cards(supply, num_players, include_colony= True)

    print("\nFinal Supply:")
    for name in supply:
        print(f"- {name} ({len(supply[name])} copies)")

    # Start the game

    game = Game(players, supply)
    game.run()

if __name__ == "__main__":
    main()