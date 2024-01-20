# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 11:15:36 2024

@author: alexa
"""

import Functions
import pandas as pd

def build_game_library(data, cum_freshness):
    #------------------DATA FILTER
    
    # Create a list to store dictionaries for each game
    games_list = []
    
    # Scatter plot for freshness benchmarks 
    freshness_thresholds = [10000, 25000, 60000, 160000, 1160000] # Star thresholds
    freshness_benchmarks = [-1, -1, -1, -1, -1] # Game number for when benchmark is surpassed
    current_game = 0
    
    # Parse Game Data 
    for game in data:
        # Filter out draws
        if game.get("result") == "draw":
            continue  # Skip this game if it's a draw
    
        # Filter out private battles
        if game.get("lobby", {}).get("name", {}).get('en_US') == "Private Battle":
            continue  # Skip this game if it's a private battle
    
        # Filter out my DCs by checking for nulls
        if game.get("kill") is None:
            continue  # Skip this game if results weren't uploaded fully
        if game.get("our_team_count") is None and game.get("rule", {}).get("name", {}).get('en_US') not in ["Turf War", "Tricolor Turf War"]:
            continue  # Skip this game if anarchy progress is None and mode is not Turf War or Tricolor Turf War
    
            
        # Get Time in Minutes
        game_time = (game.get("end_at", {}).get("time", 0) - game.get("start_at", {}).get("time", 0)) / 60 
        
        game_dict = {
            'weapon': game['weapon']['name']['en_US'],
            'time_of_game': game_time,
            'win_state': game['result'],
            'kill_permin': game.get("kill") / game_time,
            'killassist_permin': game['kill_or_assist'] / game_time,
            'death_permin': game['death'] / game_time,
            'freshness_gained': Functions.calculate_freshness(game, game_time)
        }
        
        current_game += 1
        cum_freshness += Functions.calculate_freshness(game, game_time)
        
        # Check cumtots against thresholds 
        for index in range(len(freshness_thresholds)): 
            if cum_freshness > freshness_thresholds[index]:
                if freshness_benchmarks[index] == -1:
                    freshness_benchmarks[index] = current_game
                
        games_list.append(game_dict)
        
    # Convert the list of dictionaries into a Pandas DataFrame
    games_df = pd.DataFrame(games_list)