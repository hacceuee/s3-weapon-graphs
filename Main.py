# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 15:14:32 2024

@author: hacceuee
"""

import Dependencies

# Check if dependencies are installed
if not Dependencies.check_dependencies():
    # Dependencies are not installed, ask user if they want to install
    if Dependencies.install_dependencies():
        # Try importing again after installation
        import pandas
        import matplotlib.pyplot
    else:
        # User chose not to install, exit the program or handle accordingly
        exit()
        
import json
import pandas as pd
import warnings

# Suppress DeprecationWarning related to pyarrow
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pandas")

import Functions
import KKAD_Graph
import WL_Graph
import JSON_Muncher
import Image_Saver

#check dependencys, ask user if they want to install them via #install_dependencies()or manually & restart (panda and matplotlib)

# Initialize variables outside the loop
sorted_weapons = None

Image_Saver.initialize_plot()
first_run = True

while True:
    # Load JSON data if it's the first run or if the user chooses a new file
    if first_run:
        file_path = JSON_Muncher.check_for_file()
        with open(file_path, encoding="utf8") as file:
            raw_data = json.load(file)

        # Sort and filter weapons on the first run
        weapon_counts = Functions.count_weapons(raw_data)
        sorted_weapons = Functions.sort_and_filter_weapons(weapon_counts)

    # Display sorted weapons
    Functions.display_sorted_weapons(sorted_weapons)
        
    # Cumulative freshness to be potentially modified in User Input 
    cum_freshness = 0
        
    #-------------------USER INPUT
    
    # Get user input for weapon type
    weapon_filter = None
    weapon_filter_index = input("\nEnter the number corresponding to the weapon type to filter (or press Enter to skip): ")
    
    # Filter data based on user input
    if weapon_filter_index and weapon_filter_index.isdigit():
        weapon_index = int(weapon_filter_index) - 1
        if 0 <= weapon_index < len(sorted_weapons):
            weapon_filter = sorted_weapons[weapon_index][0]
            data = [game for game in raw_data if game.get('weapon', {}).get('name', {}).get('en_US') == weapon_filter]
    else:
        data = raw_data
    
    # Generate x-axis data (number of games)
    num_games = range(1, len(data) + 1)
    
    # Ask the user for the interval (n)
    interval_input = input(f"\n------ GRAPH OPTIONS\n\nEnter the interval for printing data points (e.g., 1 for every point, 2 for every 2nd point). Max is {round((len(num_games)/2) / 5) * 5}: ")
    
    # Set the default interval to 1 if the user just presses Enter
    default_interval = 1
    max_interval_percentage = 0.5  # Maximum interval as a percentage of the number of games
    
    # Check if the input is a positive integer
    if interval_input.isdigit():
        interval = int(interval_input)
        
        # Check if the interval is within the limit
        max_allowed_interval = max(default_interval, len(num_games) * max_interval_percentage)
        interval = min(interval, max_allowed_interval)
    else:
        interval = default_interval
    
    # Ask the user if they'd like to include the star levels gained
    include_star_levels = input("\nInclude weapon star levels gained? [y/n(default)]: ").lower()
    
    # Default to not including weapon star levels if the input is not 'y' or 'n'
    include_star_levels = include_star_levels == 'y'
    
    # Possibility for pre-existing freshness levels
    if include_star_levels:
        # Freshness level mapping
        freshness_mapping = {"1*": 10000, "2*": 25000, "3*": 60000, "4*": 160000, "5*": 1160000}
    
        # Ask the user what the starting freshness level is (Enter to assume 0)
        starting_freshness_input = input("\nFreshness levels: 1* = 10,000, 2* = 25,000, 3* = 60,000, 4* = 160,000, 5* = 1,160,000\nEnter the starting star level or numerical freshness amount (press Enter to assume 0): ")
    
        # Remove commas from the input
        starting_freshness_input = starting_freshness_input.replace(',', '')
    
        # Handle the case where the input is a star level
        if starting_freshness_input in freshness_mapping:
            cum_freshness = freshness_mapping[starting_freshness_input]
        else:
            # Handle the case where the input is not a valid integer
            try:
                cum_freshness = int(starting_freshness_input) if starting_freshness_input else 0
            except ValueError:
                print("Invalid input. Please enter a valid number.")

            
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
    
    
    #------------------GRAPHS
    
    # User input for choosing the graph type
    graph_choice = input("\nAvailable graphs:\n1: Splat Stats Over Time\n2: Win Stats Over Time\n\nEnter the number corresponding to the graph type to display:")
    
    # Check user's choice and call the corresponding graph function
    if graph_choice == '1':
        KKAD_Graph.graph_KKAD(games_df, freshness_benchmarks, interval, weapon_filter, weapon_filter_index, include_star_levels)
    elif graph_choice == '2':
        WL_Graph.graph_WL(games_df, freshness_benchmarks, interval, weapon_filter, weapon_filter_index, include_star_levels)
    else:
        print("Invalid choice. Please enter either 1 or 2.")

    # Ask the user for input to restart or exit
    user_choice = input("\nDo you want to export another graph (y/n)? ").lower()

    if user_choice != 'y': # If the user doesn't enter 'yes', exit the loop
        print("\nThank you!\n\nThis project was created by hacceuee to be used with fetus_hina's https://stat.ink/. The github for this project can be found at https://github.com/hacceuee/s3-weapon-graphs. Press any key to exit.")
        # Wait for user input
        input()
        
        # End of the program
        break
    else:
        first_run = False
# TODO include private battles option
# github options (if ui) - change vertical range, change average number (from 100), toggle min number to 1 vs default 