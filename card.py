class Card:
    def __init__(self, name, cost, card_type, description, effect=None, expansion = "base"):
        self.name = name
        self.cost = cost
        self.card_type = [card_type] if isinstance(card_type, str) else card_type
        self.description = description
        self.effect = effect
        self.expansion = expansion

    def is_type(self, type_name):
        return type_name in self.card_type

    def play(self, player, game):
        if self.effect:
            self.effect(player, game)
