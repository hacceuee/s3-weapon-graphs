# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 16:57:28 2024

@author: hacceuee
"""

import math
import matplotlib.pyplot as plt

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

            
def graph_freshness(freshness_benchmarks):
    for index in range(5):
            benchmark = freshness_benchmarks[index]
            if benchmark > 0: 
                plt.axvline(benchmark, color='red', linestyle='dotted', linewidth=0.7)
                stars = '★' * (index + 1)
                
                # Calculate the position to move up by 1% of the graph height
                y_position = plt.yticks()[0][0] + 0.01 * (plt.ylim()[1] - plt.ylim()[0])
                
                # Add vertical text label directly on the line, rotated vertically
                plt.text(benchmark, y_position, f'{stars}', rotation='vertical', va='bottom', ha='right', color='red', fontsize=8)
        
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
        
def averages_display(games_df):
    # Check if the DataFrame is empty
    if games_df.empty:
        return [0, 0, 0, 0]

    # Calculate the sum of each metric
    total_kill_permin = games_df['kill_permin'].sum()
    total_killassist_permin = games_df['killassist_permin'].sum()
    total_death_permin = games_df['death_permin'].sum()
    total_wins = (games_df['win_state'] == 'win').sum()

    # Calculate the averages
    total_games = len(games_df)
    average_kill_permin = total_kill_permin / total_games
    average_killassist_permin = total_killassist_permin / total_games
    average_death_permin = total_death_permin / total_games
    average_win_percentage = (total_wins / total_games) * 100

    # Return the array of averages
    return [average_kill_permin, average_killassist_permin, average_death_permin, average_win_percentage]