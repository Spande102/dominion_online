
class Boon:
    def __init__(self, name, description, effect):
        self.name = name
        self.description = description
        self.effect = effect

def fields_gift(player, game):
    # +1 Action, +1 Coin
    player.actions += 1
    player.coins += 1
    return "+1 Action, +$1"

def seas_gift(player, game):
    # +1 Card
    player.draw_cards(1)
    return "+1 Card"

def forests_gift(player, game):
    # +1 Buy, +1 Coin
    player.buys += 1
    player.coins += 1
    return "+1 Buy, +$1"

def earths_gift(player, game):
    # You may discard a Treasure to gain a card costing up to $4.
    # Sequential Interaction using interaction_context to handle re-entrancy
    
    # Step 1: Discard Treasure (if not done)
    if not player.interaction_context.get("earths_gift_step1_done"):
        choices = player.choose_multiple_from_hand(prompt="Discard a Treasure (or none):", min_cards=0)
        # Exception raised if interaction needed
        
        # If we return, user made a choice
        if choices:
            card = choices[0]
            if "Treasure" in card.card_type:
                player.hand.remove(card)
                player.discard_pile.append(card)
                player.interaction_context["earths_gift_discarded"] = True
                player.interaction_context["earths_gift_card_name"] = card.name
            else:
                 # User selected non-treasure (or UI didn't filter). 
                 # We treat invalid discard as "no discard".
                 pass
        
        player.interaction_context["earths_gift_step1_done"] = True
        
    # Step 2: Gain Card (if discarded)
    msg = []
    if player.interaction_context.get("earths_gift_discarded"):
         discarded_name = player.interaction_context.get("earths_gift_card_name", "Treasure")
         msg.append(f"Discarded {discarded_name}")
         
         # Gain interaction
         gained_card = player.choose_from_supply(game, max_cost=4, prompt="Choose a card to gain ($4):")
         # Exception raised if interaction needed
         
         if gained_card:
             player.gain_card(gained_card)
             msg.append(f"Gained {gained_card.name}")
             
             # Cleanup Context on completion
             player.interaction_context = {}
             return ", ".join(msg)
    else:
        # Cleanup Context (didn't discard, so done)
        player.interaction_context = {}
        return "Did nothing (No treasure discarded)."

    return "Interacting..." # Should be unreachable if interactions raise exceptions


def mountains_gift(player, game):
    # Gain a Silver
    if "Silver" in game.supply and game.supply["Silver"]:
        silver = game.supply["Silver"].pop()
        player.gain_card(silver)
        print(f"{player.name} gains a Silver.")
    else:
        print("No Silvers left to gain.")

def swamps_gift(player, game):
    # Gain a Will-o'-Wisp
    # We dynamically load it to avoid circular imports if any, 
    # but here we just need to instantiate/copy it.
    from cards.nocturne.will_o_wisp import WillOWisp
    player.gain_card(WillOWisp)
    return "Gained Will-o'-Wisp"

def flames_gift(player, game):
    # Trash a card from your hand.
    # Interactive:
    choices = player.choose_multiple_from_hand(prompt="Trash a card (or none):", min_cards=0)
    if choices:
         card = choices[0]
         player.hand.remove(card)
         game.trash.append(card)
         return f"Trashed {card.name}"
    return "Trashed nothing"

def skys_gift(player, game):
    # You may discard 3 cards to gain a Gold.
    if len(player.hand) >= 3:
         choices = player.choose_multiple_from_hand(prompt="Discard 3 cards to gain a Gold (or none):", min_cards=0)
         # Note: min_cards=0 allows escaping. But we check == 3 for logic.
         if len(choices) == 3:
             for c in choices:
                 if c in player.hand: player.hand.remove(c)
                 player.discard_pile.append(c)
             
             # Gain Gold
             if "Gold" in game.supply and game.supply["Gold"]:
                 gold = game.supply["Gold"].pop()
                 player.gain_card(gold)
                 return "Discarded 3 cards. Gained Gold."
             return "Discarded 3 cards (No Gold left)."
    return "Did not discard 3 cards."

def winds_gift(player, game):
    # +2 cards, Discard 2 cards.
    player.draw_cards(2)
    choices = player.choose_multiple_from_hand(prompt="Discard 2 cards:")
    # We should enforce 2 if we can, but choose_multiple is generic.
    for c in choices:
        if c in player.hand:
             player.hand.remove(c)
             player.discard_pile.append(c)
    return f"Drew 2 cards. Discarded {len(choices)}."

def rivers_gift(player, game):
    # +1 Card at start of next turn.
    from card import Card
    class RiverBoonDuration(Card):
        def __init__(self):
             super().__init__("River's Gift (Effect)", 0, ["Duration"], "End of turn effect")
        def duration_effect(self, player, game):
             player.draw_cards(1)
             print("River's Gift: +1 Card")
    
    dummy = RiverBoonDuration()
    player.duration_in_play.append(dummy)
    return "+1 Card at start of next turn."


# Registry
BOONS = [
    Boon("The Field's Gift", "+1 Action, +$1", fields_gift),
    Boon("The Sea's Gift", "+1 Card", seas_gift),
    Boon("The Forest's Gift", "+1 Buy, +$1", forests_gift),
    Boon("The Earth's Gift", "You may discard a Treasure to gain a card costing up to $4", earths_gift),
    Boon("The Mountain's Gift", "Gain a Silver", mountains_gift),
    Boon("The Swamp's Gift", "Gain a Will-o'-Wisp", swamps_gift),
    Boon("The Flame's Gift", "You may trash a card from your hand", flames_gift),
    Boon("The Sky's Gift", "Discard 3 cards to gain a Gold", skys_gift),
    Boon("The Wind's Gift", "+2 Cards, Discard 2", winds_gift),
    Boon("The River's Gift", "+1 Card next turn", rivers_gift),
]
