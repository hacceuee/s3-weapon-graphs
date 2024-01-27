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

import Functions
import JSON_Muncher

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
        
        # QLabel fields for displaying information
        self.Mod_NumOfGames = self.findChild(QLabel, 'Mod_NumOfGames')
        self.Mod_WeaponName = self.findChild(QLabel, 'Mod_WeaponName')
        
        # Connect the signals to the custom methods
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
        
        # Connect the signal to the custom method
        self.DropDown_WeaponSelect.currentIndexChanged.connect(self.create_graph)
        
        # Show the app
        self.show()
        
        # Initialize variables
        self.cum_freshness = 0  # Initial value
        
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
        
    def update_freshness(self, value=None):
        # Enable Freshness Input if Other is selected
        self.Spin_FreshnessInput.setEnabled(self.Radio_Other.isChecked())
    
        if value is not None:
            # Update freshness when the value of Spin_FreshnessInput changes
            star_level = self.get_selected_star_level()
            self.cum_freshness = self.Spin_FreshnessInput.value()
        else:
            # Update freshness when a star selection changes
            star_level = self.get_selected_star_level()
            self.cum_freshness = self.calculate_cum_freshness(star_level)
    
        # Format cum_freshness with commas
        formatted_freshness = "{:,}".format(self.cum_freshness)
    
        # Set the text of Mod_StartingFreshness with the formatted cum_freshness
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

    def calculate_cum_freshness(self, star_level):
        # Calculate cum_freshness based on the selected star level
        freshness_values = {1: 10000, 2: 25000, 3: 60000, 4: 160000, 5: 1160000}
        return freshness_values.get(star_level, 0)
        
    def update_cumulative_benchmarks(self):
        # Reset freshness benchmarks
        freshness_thresholds = [10000, 25000, 60000, 160000, 1160000]
        freshness_benchmarks = [-1, -1, -1, -1, -1]
        current_game = 0
    
        # Parse Game Data
        for game in self.data:
            # Filter out draws, private battles, and incomplete results
            if (
                game.get("result") == "draw"
                or game.get("lobby", {}).get("name", {}).get('en_US') == "Private Battle"
                or game.get("kill") is None
                or (
                    game.get("our_team_count") is None
                    and game.get("rule", {}).get("name", {}).get('en_US') not in ["Turf War", "Tricolor Turf War"]
                )
            ):
                continue
    
            # Get Time in Minutes
            game_time = (game.get("end_at", {}).get("time", 0) - game.get("start_at", {}).get("time", 0)) / 60
    
            # Update cumulative freshness and check against thresholds
            current_game += 1
            self.cum_freshness += Functions.calculate_freshness(game, game_time)
    
            # Check cum_freshness against thresholds
            for index in range(len(freshness_thresholds)):
                if self.cum_freshness > freshness_thresholds[index]:
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
        
    def create_graph(self, index):
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
            self.Mod_NumOfGames.setText(f"{len(self.data)}")
            
        else:
            # Clear QLabel fields if "(No Filter)" is selected
            self.data = self.raw_data 
            
            self.Mod_WeaponName.clear()
            self.Mod_NumOfGames.clear()

        # Set the maximum value for the QSpinBox based on the filtered data
        max_interval_percentage = 0.3  # Maximum interval as a percentage of the number of games for the selected weapon
        max_allowed_interval = max(1, int(len(self.data) * max_interval_percentage))
        self.Label_Interval.setText(f"Graph Interval (Max - {max_allowed_interval}):")
        self.Spin_IntervalInput.setMaximum(max_allowed_interval) # Update QLabel_Interval text based on the number of games for the selected weapon
        
        
        

if __name__ == "__main__":
    app = QApplication([])
    window = Application()
    app.exec_()
