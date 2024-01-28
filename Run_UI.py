# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 13:52:08 2024

@author: hacceuee
"""

from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QLabel, QSpinBox, QDoubleSpinBox, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys
import json
import pandas as pd

import Functions
import JSON_Muncher
import KKAD_Graph
import WL_Graph
import Image_Saver

# Initialize variables outside the loop
Image_Saver.initialize_plot()

class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        
        # Load the UI file 
        uic.loadUi("Main_UI.ui", self)
        
        #------------------ LOAD ELEMENTS 
        
        file_path = JSON_Muncher.check_for_file()
        with open(file_path, encoding="utf8") as file:
            self.raw_data = json.load(file)
            
        # Get the list of weapons with counts
        weapon_counts = Functions.count_weapons(self.raw_data)
        sorted_weapons = Functions.sort_and_filter_weapons(weapon_counts)
        weapon_list = ["(No Filter)"] + [f"{weapon[0]} ({weapon[1]} games)" for weapon in sorted_weapons]

        # Populate the QComboBox
        self.DropDown_WeaponSelect = self.findChild(QComboBox, 'DropDown_WeaponSelect')
        self.DropDown_WeaponSelect.addItems(weapon_list)
        self.DropDown_WeaponSelect.currentIndexChanged.connect(self.update_data_for_selected_weapon)
        
        # Set initial count 
        self.Mod_NumOfGames.setText(f"{len(self.raw_data)}")
        
        # QLabel fields for displaying information
        self.Mod_NumOfGames = self.findChild(QLabel, 'Mod_NumOfGames')
        self.Mod_WeaponName = self.findChild(QLabel, 'Mod_WeaponName')
        
        # Connect the Weapon select signal to the custom method
        self.DropDown_WeaponSelect.currentIndexChanged.connect(self.enable_freshness_checkbox)
        
        # Connect the stateChanged signal of Check_IncludeFreshness to the custom method
        self.Check_IncludeFreshness = self.findChild(QCheckBox, 'Check_IncludeFreshness')
        self.Check_IncludeFreshness.stateChanged.connect(self.enable_freshness_widgets)
        # Connect the valueChanged signal of Spin_FreshnessInput to the custom method
        self.Spin_FreshnessInput.valueChanged[int].connect(self.update_freshness)
        # Connect the toggled signal of each radio button to the custom method
        self.Radio_1Star.toggled.connect(self.update_freshness)
        self.Radio_2Star.toggled.connect(self.update_freshness)
        self.Radio_3Star.toggled.connect(self.update_freshness)
        self.Radio_4Star.toggled.connect(self.update_freshness)
        self.Radio_5Star.toggled.connect(self.update_freshness)
        self.Radio_Other.toggled.connect(self.update_freshness)
        
        # QSpinBox for getting user input for the interval
        self.Spin_IntervalInput = self.findChild(QSpinBox, 'Spin_IntervalInput')
        
        #Update freshness and games list if the user toggles the "Include Private" button
        self.Check_IncludePrivate.stateChanged.connect(self.update_cumulative_benchmarks)
        
        # Connect the clicked signal of graph buttons to custom methods
        self.Button_KAD_Graph.clicked.connect(self.display_KKAD_graph)
        self.Button_WL_Graph.clicked.connect(self.display_WL_graph)
        
        # Show the app
        self.show()
        
        # Initialize variables
        self.starting_freshness = 0  # Initial value
        
    def build_game_dict(self):
        # Create a list to store dictionaries for each game
        games_list = []
        
        for game in self.data:
            # Check if "Check_IncludePrivate" is ticked
            include_private = self.Check_IncludePrivate.isChecked()
            
            # Filter out draws
            if game.get("result") == "draw":
                continue  # Skip this game if it's a draw
            
            # Filter out private battles if "Check_IncludePrivate" is not ticked
            if not include_private and game.get("lobby", {}).get("name", {}).get('en_US') == "Private Battle":
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
            games_list.append(game_dict)
                
        return games_list
       
    def enable_freshness_checkbox(self):
        selected_weapon = self.DropDown_WeaponSelect.currentText()

        # Enable or disable the freshness checkbox based on whether a weapon is selected
        self.Check_IncludeFreshness.setEnabled(selected_weapon != "(No Filter)")
        
    def enable_freshness_widgets (self, state):
        include_star_levels = state == Qt.Checked
        
        # Enable or disable the radio buttons based on the checkbox state
        self.Radio_1Star.setEnabled(include_star_levels)
        self.Radio_2Star.setEnabled(include_star_levels)
        self.Radio_3Star.setEnabled(include_star_levels)
        self.Radio_4Star.setEnabled(include_star_levels)
        self.Radio_5Star.setEnabled(include_star_levels)
        self.Radio_Other.setEnabled(include_star_levels)
        
        self.update_cumulative_benchmarks()
        
    def update_freshness(self, state):
        # Enable Freshness Input if Other is selected
        self.Spin_FreshnessInput.setEnabled(self.Radio_Other.isChecked())
    
        if self.Radio_Other.isChecked():
            # Update freshness when the value of Spin_FreshnessInput changes
            star_level = self.get_selected_star_level()
            self.starting_freshness = self.Spin_FreshnessInput.value()
        else:
            # Update freshness when a star selection changes
            star_level = self.get_selected_star_level()
            self.starting_freshness = self.calculate_starting_freshness(star_level)
    
        # Format starting_freshness with commas
        formatted_freshness = "{:,}".format(self.starting_freshness)
    
        # Set the text of Mod_StartingFreshness with the formatted starting_freshness
        self.Mod_StartingFreshness.setText(formatted_freshness)
    
        # Perform cumulative calculations and check against freshness benchmarks
        self.update_cumulative_benchmarks()
    
    def get_selected_star_level(self):
        # Determine the selected star level based on the radio buttons
        if self.Radio_1Star.isChecked():
            return 1
        elif self.Radio_2Star.isChecked():
            return 2
        elif self.Radio_3Star.isChecked():
            return 3
        elif self.Radio_4Star.isChecked():
            return 4
        elif self.Radio_5Star.isChecked():
            return 5
        else:
            return 0  # Default if none selected

    def calculate_starting_freshness(self, star_level):
        # Calculate starting_freshness based on the selected star level
        freshness_values = {1: 10000, 2: 25000, 3: 60000, 4: 160000, 5: 1160000}
        return freshness_values.get(star_level, 0)
        
    def update_cumulative_benchmarks(self):
        # Reset freshness benchmarks
        freshness_thresholds = [10000, 25000, 60000, 160000, 1160000]
        freshness_benchmarks = [-1, -1, -1, -1, -1]
        current_game = 0
        cum_freshness = self.starting_freshness
    
        # Parse Game Data
        for game in self.data:
            # Check if private battles should be included
            if not self.Check_IncludePrivate.isChecked() and game.get("lobby", {}).get("name", {}).get('en_US') == "Private Battle":
                continue
            
            # If private battles are included, increment current_game
            if self.Check_IncludePrivate.isChecked() and game.get("lobby", {}).get("name", {}).get('en_US') == "Private Battle":
               current_game += 1
               continue
    
            # Filter out draws
            if game.get("result") == "draw":
                continue  # Skip this game if it's a draw
            
            # Filter out my DCs by checking for nulls
            if game.get("kill") is None:
                continue  # Skip this game if results weren't uploaded fully
            if game.get("our_team_count") is None and game.get("rule", {}).get("name", {}).get('en_US') not in ["Turf War", "Tricolor Turf War"]:
                continue  # Skip this game if anarchy progress is None and mode is not Turf War or Tricolor Turf War
    
            # Get Time in Minutes
            game_time = (game.get("end_at", {}).get("time", 0) - game.get("start_at", {}).get("time", 0)) / 60
    
            # Update cumulative freshness and check against thresholds
            current_game += 1
            cum_freshness += Functions.calculate_freshness(game, game_time)
    
            # Check starting_freshness against thresholds
            for index in range(len(freshness_thresholds)):
                if cum_freshness > freshness_thresholds[index]:
                    if freshness_benchmarks[index] == -1:
                        freshness_benchmarks[index] = current_game

        # Check if the last two values were both 1 and set the previous index to -1
        for index in range(1, len(freshness_thresholds)):
            if freshness_benchmarks[index - 1] == 1 and freshness_benchmarks[index] == 1:
                freshness_benchmarks[index - 1] = -1
                
        # Update the QLabel widgets with the freshness benchmarks
        self.Mod_1Star.setText(str(freshness_benchmarks[0]) if freshness_benchmarks[0] != -1 else "N/A")
        self.Mod_2Star.setText(str(freshness_benchmarks[1]) if freshness_benchmarks[1] != -1 else "N/A")
        self.Mod_3Star.setText(str(freshness_benchmarks[2]) if freshness_benchmarks[2] != -1 else "N/A")
        self.Mod_4Star.setText(str(freshness_benchmarks[3]) if freshness_benchmarks[3] != -1 else "N/A")
        self.Mod_5Star.setText(str(freshness_benchmarks[4]) if freshness_benchmarks[4] != -1 else "N/A")
       
        return freshness_benchmarks
        
    def display_KKAD_graph(self):
        
            # Get the selected item text from the DropDown_WeaponSelect
            selected_item = self.DropDown_WeaponSelect.currentText()
            
            if selected_item != "(No Filter)":
                parts = selected_item.split()
                weapon_name = ' '.join(parts[:-2])  # Join all parts except the last two
            else: weapon_name = "All Weapons"
    
            # Get the interval from the Spin_IntervalInput
            interval = self.Spin_IntervalInput.value()
    
            # Get freshness benchmarks from the update_cumulative_benchmarks function
            freshness_benchmarks = self.update_cumulative_benchmarks()
    
            # Get include_star_levels based on the state of Check_IncludeFreshness
            include_star_levels = self.Check_IncludeFreshness.isChecked() if selected_item != "(No Filter)" else False
    
            # Call the graph_KKAD function with the required parameters
            KKAD_Graph.graph_KKAD(
                self.games_df,
                freshness_benchmarks,
                interval,
                weapon_name,
                include_star_levels
            )         

    def display_WL_graph(self):
        # Get the selected item text from the DropDown_WeaponSelect
        selected_item = self.DropDown_WeaponSelect.currentText()
        
        if selected_item != "(No Filter)":
            parts = selected_item.split()
            weapon_name = ' '.join(parts[:-2])  # Join all parts except the last two
        else: weapon_name = "All Weapons"

        # Get the interval from the Spin_IntervalInput
        interval = self.Spin_IntervalInput.value()

        # Get freshness benchmarks from the update_cumulative_benchmarks function
        freshness_benchmarks = self.update_cumulative_benchmarks()

        # Get include_star_levels based on the state of Check_IncludeFreshness
        include_star_levels = self.Check_IncludeFreshness.isChecked() if selected_item != "(No Filter)" else False
        
        # Call the graph_WL function with the required parameters
        WL_Graph.graph_WL(
            self.games_df,
            freshness_benchmarks,
            interval,
            weapon_name,
            include_star_levels
        )
        
    def update_data_for_selected_weapon(self, index):
        # Get the selected item text
        selected_item = self.DropDown_WeaponSelect.currentText()
        
        # Parse the selected item text to extract weapon name and number of games
        if selected_item != "(No Filter)":
            parts = selected_item.split()
            weapon_name = ' '.join(parts[:-2])  # Join all parts except the last two
            
            # Filter data based on the DropDown
            self.data = [game for game in self.raw_data if game.get('weapon', {}).get('name', {}).get('en_US') == weapon_name]
            
            # Generate x-axis data (number of games)
            num_games = range(1, len(self.data) + 1)
    
            # Update QLabel fields
            self.Mod_WeaponName.setText(f"{weapon_name}")
            
        else:
            # Clear QLabel fields if "(No Filter)" is selected
            self.data = self.raw_data 
            
            # Update QLabel fields
            self.Mod_WeaponName.setText("All Weapons")

        self.Mod_NumOfGames.setText(f"{len(self.data)}")

        # Set the maximum value for the QSpinBox based on the filtered data
        max_interval_percentage = 0.3  # Maximum interval as a percentage of the number of games for the selected weapon
        max_allowed_interval = max(1, int(len(self.data) * max_interval_percentage))
        self.Label_Interval.setText(f"Graph Interval (Max - {max_allowed_interval}):")
        self.Spin_IntervalInput.setMaximum(max_allowed_interval) # Update QLabel_Interval text based on the number of games for the selected weapon
        
        games_list = self.build_game_dict()
        # Convert the list of dictionaries into a Pandas DataFrame
        self.games_df = pd.DataFrame(games_list)
        
        # Make overall averages[] for the left column display
        averages = Functions.averages_display(self.games_df)
        # Assign averages to QLabel widgets
        self.Mod_AverK.setText(f"{round(averages[0], 2)}")
        self.Mod_AverKA.setText(f"{round(averages[1], 2)}")
        self.Mod_AverD.setText(f"{round(averages[2], 2)}")
        self.Mod_AverWL.setText(f"{round(averages[3], 2)}%")
            
        # Update cumulative benchmarks
        freshness_benchmarks = self.update_cumulative_benchmarks()
    
if __name__ == "__main__":
    app = QApplication([])
    window = Application()
    app.exec_()
