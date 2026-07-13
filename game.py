class Game:
    def __init__(self, players, supply):
        from cards.nocturne.boons import BOONS
        self.players = players
        self.supply = supply
        self.trash_pile = []
        self.supply_counts = {}
        
        # Boons
        self.boon_deck = list(BOONS)
        self.boon_discard = []
        import random
        random.shuffle(self.boon_deck)
        self.turn_index = 0
        self.phase = 'action' # action, buy, night, cleanup
        self.pending_interactions = [] # Queue for multi-step/multi-player interactions
        self.final_scores = None
        
        for player in self.players:
            player.deck = self.initial_deck()
            player.draw_cards(5)
            
        # Start first player's turn
        self.players[0].start_turn()

    def initial_deck(self):
        from cards.base_set.copper import Copper
        from cards.nocturne.boons import BOONS
        from cards.base_set.estate import Estate
        return [Copper for _ in range(7)] + [Estate for _ in range(3)]
        
    def current_player(self):
        return self.players[self.turn_index]

    def receive_boon(self, player):
        """Logic for a player receiving a Boon."""
        if not self.boon_deck:
            if self.boon_discard:
                print("Reshuffling Boon Deck...")
                self.boon_deck = self.boon_discard[:] # Copy
                self.boon_discard = []
                random.shuffle(self.boon_deck)
            else:
                 return "No Boons available."

        if self.boon_deck:
            boon = self.boon_deck.pop(0)
            print(f"Boon revealed: {boon.name}")
            msg = boon.effect(player, self)
            
            # Default: discard boon after use (some might persist, but default is discard)
            self.boon_discard.append(boon)
            
            return f"Received {boon.name}: {msg}"
        return "Boon deck empty."

    def get_game_state(self):
        """Returns a dictionary representing the full game state."""
        return {
            "supply": {name: [c.cost for c in pile][0] if pile else 0 for name, pile in self.supply.items()},
            "supply_counts": {name: len(pile) for name, pile in self.supply.items()},
            "players": [p.to_dict() for p in self.players],
            "trash": [c.name for c in self.trash_pile],
            "turn_index": self.turn_index,
            "current_player": self.current_player().name,
            "phase": self.phase,
            "game_over": self.is_game_over(),
            "final_scores": self.final_scores
        }

    def next_turn(self):
        self.current_player().end_turn()
        self.turn_index = (self.turn_index + 1) % len(self.players)
        self.current_player().start_turn(game=self)
        self.phase = 'action'
        
        if self.is_game_over():
            self.running = False
            self.final_scores = self.tally_scores()

    def display_supply(self):
        # Kept for debugging if needed, but UI uses get_game_state
        print("\nSupply:")
        for name, pile in self.supply.items():
            if pile:
                print(f"{name} (Cost {pile[0].cost}): {len(pile)} left")

    def topdeck_gained_card(self, player, card_name):
        if card_name in self.supply and self.supply[card_name]:
            card = self.supply[card_name].pop()
            player.deck.insert(0, card)
            return card
        return None

    def trash_card(self, card_name, zone='hand'):
         # Simplified for web context - assumes verification happened
        player = self.current_player()
        zone_list = getattr(player, zone, [])
        card = next((c for c in zone_list if c.name == card_name), None)

        if not card:
            return None

        zone_list.remove(card)
        self.trash_pile.append(card)
        return card

    def is_game_over(self):
        if not self.supply.get("Province") or len(self.supply["Province"]) == 0:
            return True
        empty_piles = sum(1 for pile in self.supply.values() if not pile)
        return empty_piles >= 3

    def check_auto_end_turn(self):
        player = self.current_player()
        if self.phase == 'buy' and player.buys == 0:
            # Check for Night cards
            has_night = any("Night" in c.card_type for c in player.hand)
            if has_night:
                self.phase = 'night'
            else:
                self.next_turn()
            return True
        return False

    def tally_scores(self):
        # Could return this instead of printing
        scores = {}
        for player in self.players:
            scores[player.name] = player.get_victory_points()
        return scores

