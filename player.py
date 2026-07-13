import random

class Player:
    def __init__(self, name):
        self.name = name
        self.deck = []
        self.hand = []
        self.discard_pile = []
        self.in_play = []

        self.actions = 1
        self.buys = 1
        self.coins = 0
        self.victory_tokens = 0

    def draw_cards(self, n=1, return_card=False):
        drawn_cards = []
        for _ in range(n):
            if not self.deck:
                self.deck = self.discard_pile
                self.discard_pile = []
                random.shuffle(self.deck)
            if self.deck:
                card = self.deck.pop()
                if return_card:
                    drawn_cards.append(card)
                else:
                    self.hand.append(card)
        if return_card:
            return drawn_cards[0] if n == 1 else drawn_cards

    def start_turn(self):
        self.actions = 1
        self.buys = 1
        self.coins = 0

    def take_turn(self, game):
        self.start_turn()
        print(f"\n-- {self.name}'s Turn --")
        print(f"Hand: {[card.name for card in self.hand]}")

        # --- Action Phase ---
        print("\n-- Action Phase --")
        while self.actions > 0 and any("Action" in card.card_type for card in self.hand):
            action_cards = [card for card in self.hand if "Action" in card.card_type]
            print(f"Actions: {self.actions}")
            print("Action Cards:")
            for i, card in enumerate(action_cards):
                print(f"{i+1}. {card.name} - {card.description}")
            choice = input("Play an action Card or Type a command \n (press Enter or type skip to skip): ").capitalize()
            if game.handle_command(self, choice):
                if not game.running:
                    return
                continue
            if choice.strip() == "" or choice.strip() == "Skip":
                break
            try:
                chosen_card = action_cards[int(choice) - 1]
            except (ValueError, IndexError):
                print("Invalid selection.")
                continue
            self.play_card(chosen_card, game)
            self.actions -= 1

        # --- Buy Phase ---
        print("\n-- Buy Phase --")
        while True:
            treasure_cards = [card for card in self.hand if "Treasure" in card.card_type]
            if not treasure_cards:
                print("No treasure cards left to play.")
                break
            print("Treasure Cards in hand:")
            for i, card in enumerate(treasure_cards):
                print(f"{i+1}. {card.name} - {card.description}")
            choice = input("Play a treasure card (enter number), or press Enter/skip to stop: ").strip()
            if choice == "" or choice.lower() == "skip":
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(treasure_cards):
                    card = treasure_cards[idx]
                    if card.effect:
                        self.coins += card.effect(self, game)
                    self.in_play.append(card)
                    self.hand.remove(card)
                    print(f"Played {card.name}. Coins: {self.coins}")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input.")

        print(f"Coins: {self.coins}")

        game.display_supply()
        while self.buys > 0:
            buy = input(f"Buy a card (coins={self.coins}) \n  Press Enter or type skip to skip: ").strip().capitalize()
            if game.handle_command(self, buy):
                if not game.running:
                    return
                continue
            if buy == "" or buy == "Skip":
                break
            if buy in game.supply and game.supply[buy] and game.supply[buy][0].cost <= self.coins:
                gained_card = game.supply[buy].pop()
                self.discard_pile.append(gained_card)
                self.coins -= gained_card.cost
                self.buys -= 1
                print(f"{self.name} bought {gained_card.name}")
            else:
                print("Invalid choice or not enough coins.")

        # --- Cleanup Phase ---
        self.cleanup()

    def play_card(self, card, game):
        self.hand.remove(card)
        self.in_play.append(card)
        if card.effect:
            card.effect(self, game)

    def choose_card_from(cards, prompt):
        if not cards:
            print("No cards available to choose from.")
            return None

        print("\n" + prompt)
        for i, card in enumerate(cards):
            print(f"{i + 1}: {card.name} - {card.description}")

        while True:
            choice = input(f"Choose a card (1-{len(cards)}) or type 0 to cancel: ").strip()
            if choice == "0":
                print("Action canceled.")
                return None  # Player chose to cancel

            try:
                index = int(choice) - 1
                if 0 <= index < len(cards):
                    chosen_card = cards[index]
                    print(f"You selected: {chosen_card.name}")
                    return chosen_card
                else:
                    print("Invalid choice. Please choose a valid card.")
            except ValueError:
                print("Invalid input. Please enter a number.")


def cleanup(self):
    print(f"{self.name}'s turn has ended.")
    self.discard_pile += self.hand + self.in_play
    self.hand = []
    self.in_play = []
    self.draw_cards(5)

def get_victory_points(self):
    all_cards = self.deck + self.hand + self.discard_pile + self.in_play
    return (
        sum(card.get_victory_points(self) if hasattr(card, "get_victory_points") else 0 for card in all_cards)
        + self.victory_tokens
    )