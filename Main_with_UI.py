# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 11:13:11 2024

@author: hacceuee
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Functions
import KKAD_Graph
import WL_Graph
import JSON_Muncher
import Game_Functions

class SplatGraphApp:
    def __init__(self, master):
        self.master = master
        master.title("Splat Graph App")

        self.first_run = True
        self.weapon_filter_var = tk.StringVar()
        self.interval_var = tk.StringVar()
        self.include_star_levels_var = tk.BooleanVar(value=True)

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Splat Graph App")
        self.label.pack()

        self.load_data_button = tk.Button(self.master, text="Load Data", command=self.load_data)
        self.load_data_button.pack()

        # Weapon Filter Input
        self.weapon_filter_label = tk.Label(self.master, text="Enter the weapon type filter (or leave blank):")
        self.weapon_filter_label.pack()
        self.weapon_filter_entry = tk.Entry(self.master, textvariable=self.weapon_filter_var)
        self.weapon_filter_entry.pack()

        # Interval Input
        self.interval_label = tk.Label(self.master, text="Enter the interval for printing data points (or leave blank for default):")
        self.interval_label.pack()
        self.interval_entry = tk.Entry(self.master, textvariable=self.interval_var)
        self.interval_entry.pack()

        # Include Star Levels Checkbutton
        self.include_star_levels_checkbox = tk.Checkbutton(self.master, text="Include weapon star levels gained?", variable=self.include_star_levels_var)
        self.include_star_levels_checkbox.pack()

        # Graph Type Input
        self.graph_type_label = tk.Label(self.master, text="Choose Graph Type:")
        self.graph_type_label.pack()

        self.kkad_button = tk.Button(self.master, text="Splat Stats Over Time", command=self.graph_KKAD)
        self.kkad_button.pack()

        self.wl_button = tk.Button(self.master, text="Win Stats Over Time", command=self.graph_WL)
        self.wl_button.pack()

        self.export_another_button = tk.Button(self.master, text="Export Another Graph", command=self.export_another)
        self.export_another_button.pack()

        self.exit_button = tk.Button(self.master, text="Exit", command=self.exit_app)
        self.exit_button.pack()

    def load_data(self):
        file_path = JSON_Muncher.check_for_file(self.first_run)
        with open(file_path, encoding="utf8") as file:
            data = json.load(file)
        self.first_run = False

    def create_dataframe(self):
        games_list = []
        cum_freshness = 0

        for game in self.data:
            Game_Functions.build_game_library(data, cum_freshness)
            pass

        games_df = pd.DataFrame(games_list)
        return games_df

    def graph_KKAD(self):
        games_df = self.create_dataframe()
        freshness_benchmarks = [10000, 25000, 60000, 160000, 1160000]  # Sample freshness thresholds
        interval = int(self.interval_var.get()) if self.interval_var.get().isdigit() else 1
        weapon_filter = self.weapon_filter_var.get()
        include_star_levels = self.include_star_levels_var.get()
        KKAD_Graph.graph_KKAD(games_df, freshness_benchmarks, interval, weapon_filter, include_star_levels)

    def graph_WL(self):
        games_df = self.create_dataframe()
        freshness_benchmarks = [10000, 25000, 60000, 160000, 1160000]  # Sample freshness thresholds
        interval = int(self.interval_var.get()) if self.interval_var.get().isdigit() else 1
        weapon_filter = self.weapon_filter_var.get()
        include_star_levels = self.include_star_levels_var.get()
        WL_Graph.graph_WL(games_df, freshness_benchmarks, interval, weapon_filter, include_star_levels)

    def export_another(self):
        self.first_run = True
        self.load_data()

    def exit_app(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SplatGraphApp(root)
    root.mainloop()