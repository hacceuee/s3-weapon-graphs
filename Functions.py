# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 16:57:28 2024

@author: hacceuee
"""

import math

def calculate_freshness(game, game_time):
    freshness = 0
    # Turf War
    if game.get("rule", {}).get("name", {}).get('en_US') in ["Turf War", "Tricolor Turf War"]:
        freshness += 300
        if game.get("result") == "win":
            freshness += 600
        inked = game.get("inked")
        if inked < 500:
            freshness += math.floor(inked / 100) * 100
        else:
            freshness += 500
    # Anarchy 
    else: 
        knockout = game.get("knockout")
        if game.get("result") == "win":
            if knockout:
                freshness += 2500
            else: 
                freshness += 1500  # Win Bonus
                freshness += math.floor(game_time) * 100  # Time Bonus
                freshness += game.get("our_team_count") * 5  # Progress Bonus
        if game.get("result") == "lose":
            freshness += math.floor(game_time) * 100  # Time Bonus
            if not knockout:
                freshness += game.get("our_team_count") * 5  # Progress Bonus
    return freshness