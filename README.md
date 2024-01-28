# s3-weapon-graphs by hacceuee

## Overview

This project allows users to visualize and analyze weapon usage and performance statistics in the game Splatoon 3. The graphs provide insights into win rates, freshness levels, and other relevant metrics for different weapons.

## Features

- Weapon usage statistics based on game data
- Graphical representation of win rates over time
- Customizable filtering for specific weapons

## Dependencies

Ensure you have the following dependencies installed:
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [PyQt5](https://pypi.org/project/PyQt5/)

If not installed, the program will prompt you to install them. You can also install them using 	`pip install -r requirements.txt`

## Getting Started

1. **Clone the repository**
	- Clone the repository to your local machine. 
	- If downloading from github, unzip the file. Navigate to the project directory.

2. **Install dependencies:**
	
	`pip install -r requirements.txt`

	- This can also be done through the program, or before-hand. 

4. **Download JSON Data:**
   - Visit [Stat.ink](https://stat.ink/) and log in to your profile.
   - Navigate to your profile and settings.
   - Export your data in JSON format (Stat.ink format, gzipped).

5. **Unzip the Downloaded File:**
   - Unzip the downloaded JSON file.

6. **Run the Program:**
   - Open the terminal or command prompt.
   - Navigate to the directory where you have the program files.

7. **Provide the JSON File Path:**
   - Run the program (`Run_UI.py`).
   - If prompted, import your .JSON file via JSON Import -> Import new file in the top menu. 

8. **Explore Graphs:**
   - The program will format and parse the JSON data.
   - USe the on-screen prompts to explore various weapon usage graphs.
   - Files are saved automatically, but you can use the tools in the visualizer and re-save the file if needed. 

9. **Export Graphs:**
   - Press the button relevant to the graph you wish to export. Graphs are saved automatically to the local file/Image Exports. You can open this folder by going to File -> Open exports folder 
   - You can save the graph with window modifications via the dialog that opens when the graph is created (last icon with the tool tip "Save the figure") 
   
## Usage

The below options provide options for generating weapon graphs.

### Graph Options: 
**Weapon Select:**
   - All weapons with >25 games recorded on stat.ink will be loaded. You may select a weapon to plot, or plot all weapons. You can only plot freshness if a weapon is selected. 

**Graph Interval:**
   - The interval (n) represents how many data points are skipped before the next one is plotted.
   - For example, an interval of 1 means every data point is plotted, while an interval of 2 means every 2nd data point is plotted. This will smooth out the graph.
     Interval of 1: ![Classic Squiffer-KD_Over_Time interval 1](https://github.com/hacceuee/s3-weapon-graphs/assets/54909901/b08fc2fc-7c5c-4fa7-b9ca-2152dc39c9a3)
     Interval of 10: ![Classic Squiffer-KD_Over_Time interval 10](https://github.com/hacceuee/s3-weapon-graphs/assets/54909901/215118ff-6866-4aef-bc4f-c2ae71f15aae)

**Freshness:**
   - Freshness markers are vertical red lines on the graphs, calculated based on game data.
   - If you choose to include freshness, the program will display freshness benchmarks as dotted red lines for better analysis.
		- You can modify the starting freshness before you started recording your games with stat.ink. You can enter an integer (ex: 160,050) or select a star level.

**Splat Stats Over Time:**
- This graph plots a running average of K/per minutes, KA/per minute, and D/per minute over the last 100 games. Because of the nature of this data analysis method, weapons with fewer than 25 games can not be plotted.

**Win Stats Over Time:**
- This graph plots a running average of your win percentage over the last 100 games. Because of the nature of this data analysis method, weapons with fewer than 25 games can not be plotted.
  Example graph (interval of 10, freshness markers included): ![Classic Squiffer-WinRates_Over_Time](https://github.com/hacceuee/s3-weapon-graphs/assets/54909901/b49b0758-d593-41cc-9b54-f29519d99fc4)

### Graph Display Options:
**Reset the view:**  ![image](https://github.com/hacceuee/s3-weapon-graphs/assets/54909901/67262823-07fc-4f55-b54b-3ffac8d0fc0e)

- Reset to the home/default view.
- Backwards to previous view (undo view).
- Forwards to next view (redo view).

**Change the view:**   ![image](https://github.com/hacceuee/s3-weapon-graphs/assets/54909901/9d2d1912-d332-4ad6-b624-39aaa6284959)

- Left button pans, right button zooms. If you hold x or y while you click with the left or right mouse button, that axis will be locked so you are only manipulating one axis. 
- Zoom to selection. If you hold x or y while you make your selection, you will keep that axis the same. 

**Axis and Graph Appearance:**  ![image](https://github.com/hacceuee/s3-weapon-graphs/assets/54909901/7277452d-866d-4835-a024-3c41e9bf00b9)

- Configure the subplot. Adjsut margins and padding. 

- Edit axis parameters.  This will allow you to change the axis scales and min/maxes (both x and y), change axis titles, and change the colors of the lines:

![image](https://github.com/hacceuee/s3-weapon-graphs/assets/54909901/092570b6-9afb-48f3-bcd8-4ef8f50f02e4)
![image](https://github.com/hacceuee/s3-weapon-graphs/assets/54909901/e33f845d-fb87-49c0-817c-19f50a66c05c)

- You can toggle between different lines on the graph with the drop-down menu:
 
 ![image](https://github.com/hacceuee/s3-weapon-graphs/assets/54909901/b3cd454f-bfa8-4ce8-8fb2-3c71ae5410db)

**Save**  ![image](https://github.com/hacceuee/s3-weapon-graphs/assets/54909901/21dfa638-3c07-4e2d-aeb4-aa4eeb8e2b4f)

- These changes aren't automatically saved. Please use the save tool to reexport the graph. 

## Feedback

If you encounter any issues or have suggestions for improvements, please open an issue on GitHub. You may also contact me on discord @dapple_dualies

## Acknowledgements

This project was created by hacceuee and is intended for use with Splatoon 3 data from [stat.ink](https://stat.ink/) by [fetus_hina](https://github.com/fetus-hina/stat.ink).
