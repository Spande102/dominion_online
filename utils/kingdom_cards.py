import random
import copy
from utils.supply_build import add_standard_cards

def choose_kingdom_cards(cards_by_expansion, interactive=False, expansion_filter=None, specific_cards=None):
    if specific_cards and len(specific_cards) > 0:
        return select_specific_cards(cards_by_expansion, specific_cards)

    if not interactive:
        # expansion_filter is a list of strings like ['Base', 'Intrigue']
        return randomize_kingdom_cards(cards_by_expansion, interactive=False, expansion_filter=expansion_filter)

    # Legacy interactive console mode (preserving just in case, or removing if undesired - assume refactor to fully API driven primarily)
    # For now, we'll keep the logic simple: if not provided specific_cards, we randomize
    return randomize_kingdom_cards(cards_by_expansion, interactive=False, expansion_filter=expansion_filter)

def randomize_kingdom_cards(cards_by_expansion, interactive=False, expansion_filter=None):
    if expansion_filter:
        # Map frontend names to backend directory names
        name_map = {
            "Base": ["base_set"], # default to base_set (2nd ed mostly)
            "Intrigue": ["intrigue"],
            "Seaside": ["seaside"],
            "Prosperity": ["prosperity"],
            "Hinterlands": ["hinterlands_1st_edition"], # only one available
            "Nocturne": ["nocturne"]
        }
        
        target_dirs = []
        for exp in expansion_filter:
            if exp in name_map:
                target_dirs.extend(name_map[exp])
            else:
                # Try direct match (lower case)
                lower = exp.lower()
                if lower in cards_by_expansion:
                    target_dirs.append(lower)
        
        # Filter existing keys
        chosen_expansions = [k for k in target_dirs if k in cards_by_expansion]
        
        if not chosen_expansions:
             # Fallback to all if invalid filter (or empty)
             chosen_expansions = list(cards_by_expansion.keys())
    else:
        chosen_expansions = list(cards_by_expansion.keys())

    # Include any card that's not a base card and intended for Kingdom use
    pool = [
        card for exp in chosen_expansions
        for card in cards_by_expansion[exp]
        if is_kingdom_card(card)
    ]

    if len(pool) < 10:
        print("Not enough eligible cards available for random selection.")
        return []

    return random.sample(pool, 10)

def manually_choose_kingdom_cards(cards_by_expansion):
    print("\nAvailable Kingdom cards:")
    all_kingdom_cards = {}

    for expansion, cards in cards_by_expansion.items():
        print(f"\n[{expansion}]")
        for card in cards:
            if is_kingdom_card(card):
                print(f" - {card.name} ({', '.join(card.card_type)})")
                all_kingdom_cards[card.name.lower()] = card

    selected_cards = []
    while len(selected_cards) < 10:
        name = input(f"\nEnter card name ({len(selected_cards) + 1}/10): ").strip().lower()
        if name in all_kingdom_cards:
            card = all_kingdom_cards[name]
            if card in selected_cards:
                print("You've already selected that card.")
            else:
                selected_cards.append(card)
        else:
            print("Card not found. Please enter the exact name shown above.")

    return selected_cards

def select_specific_cards(cards_by_expansion, specific_card_names):
    selected_cards = []
    # flattened lookup
    all_cards = {c.name.lower(): c for pool in cards_by_expansion.values() for c in pool}
    
    for name in specific_card_names:
        clean_name = name.lower().strip()
        if clean_name in all_cards:
            selected_cards.append(all_cards[clean_name])
    
    return selected_cards

# Helper: define what counts as a base Kingdom card
def is_kingdom_card(card):
    base_cards = {"Copper", "Silver", "Gold", "Estate", "Duchy", "Province", "Curse", "Platinum", "Colony"}
    non_supply_cards = {"Will-o'-Wisp"}
    return card.name not in base_cards and card.name not in non_supply_cards