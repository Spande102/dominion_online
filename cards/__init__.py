import os
import importlib

def load_cards():
    base_path = os.path.dirname(__file__)
    all_cards = []
    cards_by_expansion = {}

    for expansion in os.listdir(base_path):
        exp_path = os.path.join(base_path, expansion)
        if os.path.isdir(exp_path) and not expansion.startswith('__'):
            cards_by_expansion[expansion] = []
            for card_file in os.listdir(exp_path):
                if card_file.endswith('.py') and card_file != '__init__.py':
                    module_name = f"cards.{expansion}.{card_file[:-3]}"
                    module = importlib.import_module(module_name)
                    for attr in dir(module):
                        card = getattr(module, attr)
                        if hasattr(card, '__class__') and getattr(card, 'card_type', None):
                            all_cards.append(card)
                            cards_by_expansion[expansion].append(card)

    return all_cards, cards_by_expansion