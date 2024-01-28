# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 13:52:08 2024

@author: hacceuee
"""


import sys
import os

# Add the 'docs' folder to the Python path
docs_path = os.path.join(os.path.dirname(__file__), 'docs')
sys.path.append(docs_path)

import Dependencies

# Check if dependencies are installed
if not Dependencies.check_dependencies():
    # Dependencies are not installed, ask user if they want to install
    if Dependencies.install_dependencies():
        # Try importing again after installation
        import pandas
        import matplotlib.pyplot
        import PyQt5
    else:
        # User chose not to install, exit the program or handle accordingly
        exit()
        
import json
import pandas as pd
import warnings

# Suppress DeprecationWarning related to pyarrow
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pandas")
# Supress loop warning


from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QLabel, QSpinBox, QDoubleSpinBox, QCheckBox, QFileDialog, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import uic
from PyQt5.QtGui import QDesktopServices

import threading

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
        ui_file_path = os.path.join(docs_path, "Main_UI.ui")
        uic.loadUi(ui_file_path, self)
        
        # Access the existing progress bar
        self.ProgressBar_Loading = self.findChild(QProgressBar, "ProgressBar_Loading")
        self.ProgressBar_Loading.hide()  # Initially hide the progress bar
        
        #------------------ CONNECT ACTIONS
        self.DropDown_WeaponSelect = self.findChild(QComboBox, 'DropDown_WeaponSelect')
        self.DropDown_WeaponSelect.currentIndexChanged.connect(self.update_data_for_selected_weapon)
        
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
        
        # Connect the menu action to the update_file_path method
        self.actionImport_new_file.triggered.connect(self.update_file_path)
        self.actionReload_file.triggered.connect(self.reload_file)
        # Connect exit option
        self.actionExit.triggered.connect(self.exit_program)
        # Set up other menu actions
        self.actionOpen_file_location.triggered.connect(self.open_file_location)
        self.actionGitHub.triggered.connect(self.open_github)
        self.actionOpen_exports_folder.triggered.connect(self.open_image_location)
        
        # Initialize variables
        self.starting_freshness = 0  # Initial value
        
        # Print starting message to the terminal
        print("Starting program...")
        
        # Load database
        file_path = JSON_Muncher.check_for_file()
        self.ProgressBar_Loading.setRange(0, 0)
        self.start_loading_thread(file_path) # Start the loading thread
        
        # Show the app
        self.show()
        
        # Print message to the terminal indicating that the program has started
        print("\rProgram running.")
    
    def start_loading_thread(self, file_path):
        # Show the progress bar when loading starts
        self.ProgressBar_Loading.show()
    
        # Start a new thread for loading the file
        loading_thread = threading.Thread(target=self.load_file, args=(file_path,))
        loading_thread.start()
        
    def load_file (self, file_path):
        try: 
            if file_path is not None:
                with open(file_path, encoding="utf8") as file:
                    self.raw_data = json.load(file)
                
                # Get the list of weapons with counts
                weapon_counts = Functions.count_weapons(self.raw_data)
                sorted_weapons = Functions.sort_and_filter_weapons(weapon_counts)
                self.weapon_list = ["(No Filter)"] + [f"{weapon[0]} ({weapon[1]} games)" for weapon in sorted_weapons]
                
                # Clear existing items in QComboBox
                self.DropDown_WeaponSelect.clear()
        
                # Populate the QComboBox with updated items
                self.DropDown_WeaponSelect.addItems(self.weapon_list)
                
                # Set initial count 
                self.Mod_NumOfGames.setText(f"{len(self.raw_data)}")
                self.Mod_FilePath.setText(file_path)
                
                self.player_name = self.raw_data[-1].get('user', {}).get('name')
                self.Mod_PlayerName.setText(f"Games processed for: {self.player_name}")
                self.Mod_PlayerName.setStyleSheet("color: rgba(0, 0, 0, 128);") 
                
            else: 
                self.Label_User_Updates.setText("Import a .JSON file by navigating to 'JSON Import -> Import new file.' \nEnsure that the file has been downloaded and unzipped from the Export feature on your profile at stat.ink.")
                self.Label_User_Updates.setStyleSheet("color: rgba(135, 32, 28, 255); font-weight: bold;")
            
        except json.JSONDecodeError:
            # If there's an error loading the file during startup, set the initial message
            self.Label_User_Updates.setText("Import a .JSON file by navigating to 'JSON Import -> Import new file.' \nEnsure that the file has been downloaded and unzipped from the Export feature on your profile at stat.ink.")
            self.Label_User_Updates.setStyleSheet("color: rgba(135, 32, 28, 255); font-weight: bold;")
        
        # Reset the progress bar value after loading is done
        self.ProgressBar_Loading.setValue(0)
        
        # Hide the progress bar when loading is done
        self.ProgressBar_Loading.hide()
    
    def reload_file (self):
        # Load database
        file_path = JSON_Muncher.check_for_file()
        self.ProgressBar_Loading.setRange(0, 0)
        self.start_loading_thread(file_path) # Start the loading thread
        
        self.Label_User_Updates.setText(f"{file_path} has been reloaded.")
        self.Label_User_Updates.setStyleSheet("color: rgba(0, 0, 0, 128);") 
    
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
            printed_file = KKAD_Graph.graph_KKAD(
                self.games_df,
                freshness_benchmarks,
                interval,
                weapon_name,
                include_star_levels,
                self.player_name
            )     
            
            self.Label_User_Updates.setText(f"Graph has automatically been saved as {printed_file}")
            self.Label_User_Updates.setStyleSheet("color: rgba(0, 0, 0, 128);") 

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
        printed_file = WL_Graph.graph_WL(
            self.games_df,
            freshness_benchmarks,
            interval,
            weapon_name,
            include_star_levels,
            self.player_name
        )
        
        self.Label_User_Updates.setText(f"Graph has automatically been saved as {printed_file}")
        self.Label_User_Updates.setStyleSheet("color: rgba(0, 0, 0, 128);") 
        
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
    
    def update_file_path(self, file_path):
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "JSON File (*.json);; All Files (*)")
        
        # Pass file_path to JSON muncher
        if file_path: 
            new_path = JSON_Muncher.import_new_file(file_path)
            # Set the progress bar to indeterminate mode while loading
            self.ProgressBar_Loading.setRange(0, 0)
            self.start_loading_thread(new_path) # Start the loading thread
            self.Label_User_Updates.setText(f"{file_path} has successfully been parsed and copied to {new_path}")
            self.Label_User_Updates.setStyleSheet("color: rgba(0, 0, 0, 128);") 
    
    def open_file_location(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        try:
            # Open file location in the default file manager
            QDesktopServices.openUrl(QUrl.fromLocalFile(script_directory))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error opening file location: {str(e)}")

    def open_github(self):
        try:
            # Open GitHub link in the default web browser
            QDesktopServices.openUrl(QUrl("https://github.com/hacceuee/s3-weapon-graphs"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error opening GitHub link: {str(e)}")

    def open_image_location(self):
            try:
                # Specify the path to the image location folder
                image_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Image Exports")
    
                # Open image location folder in the default file manager
                QDesktopServices.openUrl(QUrl.fromLocalFile(image_folder_path))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error opening image location: {str(e)}")
        
    def exit_program(self):
        print("\rProgram terminated.")
        self.close()
            
    
if __name__ == "__main__":
    app = QApplication([])
    window = Application()
    app.exec_()
