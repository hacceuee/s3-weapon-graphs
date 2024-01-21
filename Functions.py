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

def count_weapons(data):
    weapon_counts = {}
    for game in data:
        weapon_name = game.get('weapon', {}).get('name', {}).get('en_US')
        if weapon_name:
            weapon_counts[weapon_name] = weapon_counts.get(weapon_name, 0) + 1
    return weapon_counts

def sort_and_filter_weapons(weapon_counts, min_games=25):
    # Sort weapons by usage count
    sorted_weapons = sorted(weapon_counts.items(), key=lambda x: x[1], reverse=True)

    # Filter weapons with less than min_games
    sorted_weapons = [(weapon, count) for weapon, count in sorted_weapons if count >= min_games]

    return sorted_weapons

def display_sorted_weapons(sorted_weapons):
    print("\n------ FILTER OPTIONS\n\nWeapons need 25 or more games to make a graph.\n")
    for i, (weapon, count) in enumerate(sorted_weapons, start=1):
        print(f"{i}: {weapon} ({count} games)")