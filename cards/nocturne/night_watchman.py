from card import Card

def night_watchman_effect(player, game):
    # Look at the top 5 cards of your deck, discard any number, put the rest back on top in any order
    
    cards = []
    for _ in range(5):
        if player.deck:
            cards.append(player.deck.pop())
        elif player.discard_pile: # reshuffle logic handled in draw usually but manual here
             # manual reshuffle for picking
             player.deck = player.discard_pile
             player.discard_pile = []
             import random
             random.shuffle(player.deck)
             if player.deck:
                 cards.append(player.deck.pop())
                 
    print(f"Night Watchman sees: {[c.name for c in cards]}")
    # Auto-discard logic or just put back?
    # Let's put them back for now to be safe.
    for c in reversed(cards):
        player.deck.append(c)
        
    print("Night Watchman: Top 5 cards returned.")
    
    return f"Looked at 5 cards."

NightWatchman = Card(
    "Night Watchman",
    cost=3,
    card_type=["Night"],
    description="Look at the top 5 cards of your deck, discard any number, and put the rest back on top in any order. This is gained to your hand (instead of your discard pile).",
    effect=night_watchman_effect,
    expansion="nocturne"
)
