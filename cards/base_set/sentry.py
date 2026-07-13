from card import Card
from player import InteractionRequired

def sentry_effect(player, game):
    # +1 Card, +1 Action (Handled by framework? No, usually cards handle their own basic effects if custom?)
    # Wait, usually `play_card` handles basic stats if they are properties. 
    # But `sentry.py` defines them in the card object, so the framework adds them?
    # Let's check `card.py` or `player.py`. 
    # Re-reading `player.py`: `play_action_card` adds actions/buys/coins from the Card object.
    # So we just need the "Look at top 2..." part here.
    
    player.draw_cards(1)
    player.actions += 1

    # Look at top 2 cards
    # We "draw" them to look at them, but they are technically separate from hand until we put them back?
    # Or strict Dominion rule: "Look at". They are not in hand. 
    # We'll temporarily pop them from deck.
    
    top_cards = []
    for _ in range(2):
        if player.deck:
            top_cards.append(player.deck.pop(0))
        elif player.discard_pile:
            # Trigger shuffle if needed?
            # Player.draw_card handles shuffle. Let's use internal method if available or simulate it.
            # Player.draw_cards joins hand.
            # Let's use `player.draw_card()` helper if it exists, or just logic from `draw_cards`.
            # `draw_cards` appends to hand.
            # Let's manually handle shuffle if deck empty.
            from random import shuffle
            player.deck = player.discard_pile[:]
            player.discard_pile = []
            shuffle(player.deck)
            if player.deck:
                top_cards.append(player.deck.pop(0))
    
    # Filter Nones if any weirdness (shouldn't be if logic is sound)
    
    if not top_cards:
        return # Nothing to do

    # We need to send these card names/types to client
    cards_data = [{"name": c.name, "type": c.card_type, "cost": c.cost} for c in top_cards]

    def resolve_sentry(p, g, result):
        # result is { 'trash': [name1], 'discard': [name2], 'top_deck': [name3, name4] }
        trash_names = result.get('trash', [])
        discard_names = result.get('discard', [])
        top_deck_names = result.get('top_deck', [])
        
        # We need to map names back to the card objects in `top_cards`
        # Be careful of duplicates (e.g. 2 Coppers)
        
        current_pool = top_cards[:]
        
        # Process Trash
        for name in trash_names:
            found = next((c for c in current_pool if c.name == name), None)
            if found:
                game.trash_pile.append(found)
                current_pool.remove(found)
        
        # Process Discard
        for name in discard_names:
            found = next((c for c in current_pool if c.name == name), None)
            if found:
                p.discard_pile.append(found)
                current_pool.remove(found)
        
        # Process Top Deck (Reorder)
        # The client sends the order they want.
        # We assume `top_deck_names` contains the remaining cards in order (top first).
        
        # First, ensure we only re-add what is actually left in current_pool
        # (Security check: client shouldn't be able to generate cards)
        
        reversed_order = [] # We insert at 0, so we want the LAST card of the top-to-bottom list inserted FIRST.
        
        # It's easier to reconstruct the list in order, then insert them.
        final_order = []
        
        for name in top_deck_names:
            found = next((c for c in current_pool if c.name == name), None)
            if found:
                final_order.append(found)
                current_pool.remove(found)
        
        # If anything remains (e.g. client didn't send full list), append it?
        final_order.extend(current_pool)
        
        # Now put back on deck. 
        # Deck[0] is top.
        # So we insert the last item of final_order at 0, then...
        # Wait, if `final_order` is [A, B] where A is top.
        # Deck should be [A, B, ...]
        # So we insert B at 0, then A at 0.
        
        for card in reversed(final_order):
            p.deck.insert(0, card)

    raise InteractionRequired(
        "sentry_resolution",
        "Sentry: Look at top 2 cards. Trash/Discard any. Reorder rest.",
        cards=cards_data,
        callback=resolve_sentry
    )

Sentry = Card(
    "Sentry",
    cost=5,
    card_type=["Action"],
    description="Look at the top 2 cards of your deck. Trash and/or discard any number. Put the rest back in any order.",
    effect=sentry_effect,
    expansion="base"
)