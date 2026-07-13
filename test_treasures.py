from game import Game
from player import Player
from cards import load_cards
from utils.supply_build import add_standard_cards
from utils.kingdom_cards import choose_kingdom_cards
import json

def test_granular_treasure():
    print("Initializing Game for Treasure Test...")
    all_cards, cards_by_expansion = load_cards()
    players = [Player("Player 1"), Player("Player 2")]
    
    # Setup robust supply
    selected_kingdom_cards = choose_kingdom_cards(cards_by_expansion, interactive=False)
    supply = {card.name: [card for _ in range(10)] for card in selected_kingdom_cards}
    add_standard_cards(supply, len(players), include_colony=False)
    
    game = Game(players, supply)
    p1 = game.current_player()
    
    print(f"\nInitial Hand: {[c.name for c in p1.hand]}")
    
    # Find a Copper
    copper = next((c for c in p1.hand if c.name == "Copper"), None)
    if not copper:
        print("No Copper in opening hand, forcing one for test.")
        from cards.base_set.copper import Copper
        p1.hand.append(Copper) # Direct add for test
        copper = Copper

    print(f"Playing 1 Copper...")
    # Simulate server logic: check type then call play_treasure
    if "Treasure" in copper.card_type:
        success, msg = p1.play_treasure("Copper", game)
        print(f"Result: {success} - {msg}")
        if success:
             game.phase = 'buy'
    
    assert p1.coins == 1
    assert game.phase == 'buy'
    print("Verified: phase is 'buy' and coins == 1 after playing 1 Copper.")
    
    # Play another if available
    count_hand_copper = len([c for c in p1.hand if c.name == "Copper"])
    print(f"Coppers remaining in hand: {count_hand_copper}")
    
    if count_hand_copper > 0:
         success, msg = p1.play_treasure("Copper", game)
         print(f"Played second copper: {success} - {msg}")
         assert p1.coins == 2
         
    print("\nGranular Treasure Test Passed!")

if __name__ == "__main__":
    try:
        test_granular_treasure()
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
