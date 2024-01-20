# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 01:52:23 2024

@author: alexa
"""

import os
import math
import matplotlib.pyplot as plt

def set_plot_size():
    # Adjust layout to add space between the header and the graph
    plt.tight_layout(pad=2.0)
    plt.rcParams["figure.figsize"]=[10,6]
    plt.rcParams["figure.dpi"]=300  

def save_image(plt, num_games, file_name, title, subheader):

    #Axis and legend formatting
    plt.legend(fontsize=9, handlelength=1)
    plt.xlim(0-math.ceil(len(num_games)/50)+7, math.ceil(len(num_games)+len(num_games)/50))
    
    # Create text elements with different font sizes
    title_text = plt.text(0.5, 1.05, title, fontsize=18, ha='center', va='bottom', transform=plt.gca().transAxes)
    subheader_text = plt.text(0.5, 1.01, subheader, fontsize=9, ha='center', va='bottom', transform=plt.gca().transAxes)
    
    #------------------SAVING FILE
    # Create a folder if it doesn't exist
    folder_name = "Image Exports"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        
    # Specify the file path within the folder
    file_path = os.path.join(folder_name, file_name)

    plt.savefig(file_path, dpi=300)
    print(f"\nFile saved at {file_path}")
    
    # Display the plot
    plt.show()