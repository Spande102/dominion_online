from card import Card

def den_of_sin_effect(player, game):
    # +2 Cards
    player.draw_cards(2)
    
def den_of_sin_duration(player, game):
    # At start of next turn: +2 Cards
    player.draw_cards(2)
    print(f"{player.name} gets +2 Cards from Den of Sin duration.")

DenOfSin = Card(
    "Den of Sin",
    cost=5,
    card_type=["Night", "Duration"],
    description="+2 Cards. At the start of your next turn, +2 Cards.",
    effect=den_of_sin_effect,
    expansion="nocturne"
)

# Attach duration method to the instance 
DenOfSin.duration_effect = den_of_sin_duration
