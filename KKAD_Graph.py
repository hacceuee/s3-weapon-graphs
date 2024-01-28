# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 19:17:39 2024

@author: hacceuee
"""

import matplotlib.pyplot as plt

import Image_Saver
import Functions

def graph_KKAD(games_df, freshness_benchmarks, interval, weapon_name, include_star_levels):

    # Calculate the rolling average
    window_size = 100
    rolling_df = games_df[['kill_permin', 'killassist_permin', 'death_permin']].rolling(window=window_size, min_periods=25).mean()
    
    # Fill missing values in rolling_df with the average of the first 25 games
    rolling_df = rolling_df.fillna(rolling_df.iloc[:25].mean())
    
    # Generate x-axis data (number of games)
    num_games = range(1, len(games_df) + 1)
        
    # Plotting the lines
    plt.plot(num_games[::interval], rolling_df['kill_permin'][::interval], label='Kill per minute', color='blue')
    plt.plot(num_games[::interval], rolling_df['killassist_permin'][::interval], label='Kill/Assist per minute', color='blue', linestyle='dashed', linewidth=0.8)
    plt.plot(num_games[::interval], rolling_df['death_permin'][::interval], label='Death per minute', color='orange')
    
    # Add Freshness lines 
    if include_star_levels: 
        Functions.graph_freshness(freshness_benchmarks)
        
    #------------------GRAPH STUFF
    # Prepare subheader with weapon info, number of games, and interval
    subheader = f"{weapon_name} | Number of Games: {len(num_games)+1} | Interval: {interval}"
    
    # Set up the title with subheader
    title = "Splat Stats Over Time"
    
    # Adding labels and legend
    plt.xlabel('Number of Games')
    plt.ylabel('Rates per Minute')
            
    file_name = f"{weapon_name}-KD_Over_Time.png"
    Image_Saver.save_image(num_games, file_name, title, subheader)