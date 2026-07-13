def add_standard_cards(supply, num_players=2, include_colony=False):
    from cards.base_set.copper import Copper
    from cards.base_set.silver import Silver
    from cards.base_set.gold import Gold
    from cards.base_set.estate import Estate
    from cards.base_set.duchy import Duchy
    from cards.base_set.province import Province
    from cards.base_set.curse import Curse

    if include_colony:
        from cards.prosperity.platinum import Platinum
        from cards.prosperity.colony import Colony

    # Treasures
    supply["Copper"] = [Copper for _ in range(60)]
    supply["Silver"] = [Silver for _ in range(40)]
    supply["Gold"]   = [Gold for _ in range(30)]



    # Victory cards
    if num_players == 2:
        victory_count = 8
    elif num_players <= 4:
        victory_count = 12
    elif num_players == 5:
        victory_count = 15
    else: # 6 players
        victory_count = 18

    supply["Estate"]   = [Estate for _ in range(victory_count)]
    supply["Duchy"]    = [Duchy for _ in range(victory_count)]
    supply["Province"] = [Province for _ in range(victory_count)]


    if include_colony:
        supply["Platinum"] = [Platinum for _ in range(12)]
        supply["Colony"] = [Colony for _ in range(victory_count)]

    # Curses
    curse_count = (num_players - 1) * 10
    supply["Curse"] = [Curse for _ in range(curse_count)]