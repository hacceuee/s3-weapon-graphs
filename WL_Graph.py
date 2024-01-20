# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 21:27:09 2024

@author: hacceuee

"""
import matplotlib.pyplot as plt
import math

import Image_Saver

def graph_WL(games_df, freshness_benchmarks, interval, weapon_filter, weapon_filter_index, include_star_levels):
    
    # Calculate the rolling sum of wins and total games
    window_size = 100
    games_df['rolling_wins'] = games_df['win_state'].eq('win').rolling(window=window_size, min_periods=10).sum()
    games_df['rolling_total_games'] = games_df['win_state'].rolling(window=window_size, min_periods=10).count()
    
    # Calculate the rolling win percentage
    games_df['rolling_win_percentage'] = games_df['rolling_wins'] / games_df['rolling_total_games']
    
    # Fill missing values in the rolling_win_percentage column with the average of the first 10 games
    games_df['rolling_win_percentage'] = games_df['rolling_win_percentage'].fillna(games_df['rolling_win_percentage'][:10].mean())
        
    # Generate x-axis data (number of games)
    num_games = range(1, len(games_df) + 1)
    
    # Add Freshness lines 
    if include_star_levels: 
        for index in range(0,5):
            if freshness_benchmarks[index] > 0: 
                plt.axvline(freshness_benchmarks[index], color='red', linestyle='dotted', linewidth=0.7)
    
    # Plotting the rolling win percentage
    plt.plot(num_games[::interval], games_df['rolling_win_percentage'][::interval], label='Average Win Percentage (n=100 games)', color='green')
    
    
    #------------------GRAPH STUFF
    subheader = ""
    # Prepare subheader with weapon info, number of games, and interval
    if weapon_filter_index and weapon_filter_index.isdigit():
        subheader += f"Weapon: {weapon_filter} | "
    else: 
        subheader += "All Weapons | "
    subheader += f"Number of Games: {len(num_games)+1} | Interval: {interval}"
    
    # Set up the title with subheader
    title = "Win Stats Over Time"
    
    # Adding labels and legend
    plt.xlabel('Number of Games')
    plt.ylabel('Average Win Percentage')
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}')) # Adjust y axis to be %s
    
    file_name = f"{weapon_filter}-WinRates_Over_Time.png"
    Image_Saver.save_image(plt, num_games, file_name, title, subheader)

