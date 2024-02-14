# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 19:17:39 2024

@author: hacceuee
"""

import matplotlib.pyplot as plt

import Image_Saver
import math
import Functions

def graph_KKAD(games_df, freshness_benchmarks, preferences_array, line_pref, weapon_name, include_star_levels, player_name):

    # Clear the existing graph
    plt.clf()
    
    # Calculate the rolling average
    window_size = preferences_array[1]
    rolling_df = games_df[['kill_permin', 'killassist_permin', 'death_permin']].rolling(window=window_size, min_periods=math.floor(window_size/10)).mean()
    
    # Fill missing values in rolling_df with the average of the first games
    rolling_df = rolling_df.fillna(rolling_df.iloc[:math.floor(window_size/10)].mean())
    
    # Generate x-axis data (number of games), starting from the game defined by preferences_array[2]
    starting_game = preferences_array[2]
    displayed_num_games = range(starting_game, len(games_df) + 1)
    total_num_games = range(1, len(games_df) + 1)
    
    interval = preferences_array[0]
    
    # Plotting the lines, starting from the specified game
    if line_pref[0]:
        plt.plot(displayed_num_games[::interval], rolling_df['kill_permin'].iloc[starting_game-1::interval], label='Kill per minute', color='blue')
    if line_pref[1]:
        plt.plot(displayed_num_games[::interval], rolling_df['killassist_permin'].iloc[starting_game-1::interval], label='Kill/Assist per minute', color='blue', linestyle='dashed', linewidth=0.8)
    if line_pref[2]:
        plt.plot(displayed_num_games[::interval], rolling_df['death_permin'].iloc[starting_game-1::interval], label='Death per minute', color='orange')
    
    # Add Freshness lines 
    if include_star_levels: 
        Functions.graph_freshness(freshness_benchmarks, starting_game)
        
    #------------------GRAPH STUFF
    # Prepare subheader with weapon info, number of games, and interval
    subheader = f"{weapon_name} | Number of Games Shown: {len(displayed_num_games)+1}/{len(total_num_games)+1} | Interval: {interval} | Rolling Window Size: {window_size} | Player: {player_name}"
    
    # Set up the title with subheader
    title = "Splat Stats Over Time"
    
    # Adding labels and legend
    plt.xlabel('Number of Games')
    plt.ylabel('Rates per Minute')
    
    true_game_number = range(1, len(games_df) + 1)
    
    file_name = f"{weapon_name}-KD_Over_Time.png"
    Image_Saver.save_image(true_game_number, starting_game, file_name, title, subheader)
    
    return file_name