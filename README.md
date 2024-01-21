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
   - Run the program (`main.py`).
   - When prompted, enter the path to your unzipped JSON file.

8. **Explore Graphs:**
   - The program will format and parse the JSON data.
   - Follow the on-screen prompts to explore various weapon usage graphs.
   - Files are saved automatically, but you can use the tools in the visualizer and re-save the file if needed. 
   
## Usage

Follow the prompts to load game data and generate weapon graphs.

### Graph Options: 
Graph Interval: 
   - During the graphing process, you'll be prompted to set the interval for data points on the graph.
   - The interval (n) represents how many data points are skipped before the next one is plotted.
   - For example, an interval of 1 means every data point is plotted, while an interval of 2 means every 2nd data point is plotted. This will smooth out the graph.
     Interval of 1: ![Classic Squiffer-KD_Over_Time interval 1](https://github.com/hacceuee/s3-weapon-graphs/assets/54909901/b08fc2fc-7c5c-4fa7-b9ca-2152dc39c9a3)
     Interval of 10: ![Classic Squiffer-KD_Over_Time interval 10](https://github.com/hacceuee/s3-weapon-graphs/assets/54909901/215118ff-6866-4aef-bc4f-c2ae71f15aae)

Freshness:
   - You'll also be prompted to include freshness markers.
   - Freshness markers are vertical red lines on the graphs, calculated based on game data.
   - If you choose to include freshness, the program will display freshness benchmarks as dotted red lines for better analysis.
		- You can modify the starting freshness before you started recording your games with stat.ink. You can enter an integer (ex: 160,050) or a star level (ex: 3* or 4*)

** Splat Stats Over Time **
- This graph plots a running average of K/per minutes, KA/per minute, and D/per minute over the last 100 games. Because of the nature of this data analysis method, weapons with fewer than 25 games can not be plotted.

**Win Stats Over Time **
- This graph plots a running average of your win percentage over the last 100 games. Because of the nature of this data analysis method, weapons with fewer than 25 games can not be plotted.
  Example graph (interval of 10, freshness markers included): ![Classic Squiffer-WinRates_Over_Time](https://github.com/hacceuee/s3-weapon-graphs/assets/54909901/b49b0758-d593-41cc-9b54-f29519d99fc4)

## Feedback

If you encounter any issues or have suggestions for improvements, please open an issue on GitHub. You may also contact me on discord @dapple_dualies

## Acknowledgements

This project was created by hacceuee and is intended for use with Splatoon 3 data from [stat.ink](https://stat.ink/) by [fetus_hina](https://github.com/fetus-hina/stat.ink).
