# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 21:27:09 2024

@author: hacceuee

"""
import matplotlib.pyplot as plt
import numpy as np
import math

import Image_Saver
import Functions

def graph_WL(games_df, freshness_benchmarks, preferences_array, trendline_pref, weapon_name, include_star_levels, player_name):
    
    # Clear the existing graph
    plt.clf()
    
    # Calculate the rolling sum of wins and total games
    window_size = preferences_array[1]
    games_df['rolling_wins'] = games_df['win_state'].eq('win').rolling(window=window_size, min_periods=math.floor(window_size/10)).sum()
    games_df['rolling_total_games'] = games_df['win_state'].rolling(window=window_size, min_periods=math.floor(window_size/10)).count()
    
    # Calculate the rolling win percentage
    games_df['rolling_win_percentage'] = games_df['rolling_wins'] / games_df['rolling_total_games']
    
    # Fill missing values in the rolling_win_percentage column with the average of the first games
    games_df['rolling_win_percentage'] = games_df['rolling_win_percentage'].fillna(games_df['rolling_win_percentage'][:math.floor(window_size/10)].mean())
        
    # Generate x-axis data (number of games), starting from the game defined by preferences_array[2]
    starting_game = preferences_array[2]
    displayed_num_games = range(starting_game, len(games_df) + 1)
    total_num_games = range(1, len(games_df) + 1)
    
    interval = preferences_array[0]
    
    # Plotting the rolling win percentage
    plt.plot(displayed_num_games[::interval], games_df['rolling_win_percentage'].iloc[starting_game-1::interval], label=f'Rolling Win Percentage (n = {window_size})', color='green')
    
    if trendline_pref: 
        # Calculate the trendline for the entire data
        coefficients = np.polyfit(total_num_games, games_df['rolling_win_percentage'], 1)
        trendline = np.polyval(coefficients, total_num_games)
        
        # Plot the trendline, starting from the specified game
        plt.plot(total_num_games[starting_game-1:], trendline[starting_game-1:], label='Trendline', linestyle='--', color='#8cc2b3')
    
    # Add Freshness lines 
    if include_star_levels: 
        Functions.graph_freshness(freshness_benchmarks, starting_game)
    
    #------------------GRAPH STUFF
    # Prepare subheader with weapon info, number of games, and interval
    subheader = f"{weapon_name} ┃┃ Number of Games Shown: {len(displayed_num_games)+1}/{len(total_num_games)+1} ┃┃ Interval: {interval} ┃┃ Rolling Window Size: {window_size} ┃┃ Player: {player_name}"
    
    # Set up the title with subheader
    title = "Win Stats Over Time"
    
    # Adding labels and legend
    plt.xlabel('Number of Games')
    plt.ylabel('Average Win Percentage')
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}')) # Adjust y axis to be %s
    
    true_game_number = range(1, len(games_df) + 1)
    
    file_name = f"{weapon_name}-WinRates_Over_Time.png"
    Image_Saver.save_image(true_game_number, starting_game, file_name, title, subheader)
    
    return file_name
