# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 01:52:23 2024

@author: hacceuee
"""

import os
import math
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import shutil

    
def initialize_plot():
    
    # Adjust layout to add space between the header and the graph
    plt.tight_layout(pad=2.0)
    plt.rcParams["figure.figsize"]=[16,9]
    plt.rcParams["figure.dpi"]=72 
    plt.rcParams["figure.subplot.top"] = 0.85 # Set the default subplot top parameter to hopefully avoid cropping
    
    # Create a dummy plot and save it
    plt.plot([0, 1], [0, 1])
    plt.title("Temp Plot")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.savefig("temp_plot.png")
    plt.close()
    
def change_matplotlib_font():
    # Get the directory path where the Python file is located
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to the font file
    font_file = os.path.join(current_directory, 'FOT-RodinNTLG Pro DB.otf')
    
    # Add font to font manager
    fm.fontManager.addfont(font_file)

    font_name = fm.FontProperties(fname=font_file).get_name()
    plt.rcParams['font.family'] = font_name
    print("Font family: ", plt.rcParams['font.family'])
    
def save_image(num_games, starting_game, file_name, title, subheader):

    #Axis and legend formatting
    plt.legend(fontsize=9, handlelength=1)
    plt.xlim(max(0 - math.ceil(len(num_games) / 50) + 7, starting_game - math.ceil(starting_game/50)), math.ceil(len(num_games)+len(num_games)/50))
    
    plt.grid(axis="y", linestyle='--', linewidth=0.5, color='lightgrey')
    
    # Create text elements with different font sizes
    title_text = plt.text(0.5, 1.05, title, fontsize=18, ha='center', va='bottom', transform=plt.gca().transAxes)
    subheader_text = plt.text(0.5, 1.01, subheader, fontsize=9, ha='center', va='bottom', transform=plt.gca().transAxes)
    
    #------------------SAVING FILE
    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Move up one directory to the parent folder
    parent_directory = os.path.dirname(script_directory)
    
    # Join the parent directory with the desired subfolder
    folder_name = os.path.join(parent_directory, "Image Exports")
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Specify the file path within the folder
    file_path = os.path.join(folder_name, file_name)
    
    #plt.rcParams["figure.subplot.top"] = 0.85 # Set the default subplot top parameter to hopefully avoid cropping

    plt.savefig(file_path)
    print(f"\nFile saved at {file_path}")
    
    # Display the plot
    plt.show()