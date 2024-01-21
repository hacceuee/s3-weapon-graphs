# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 11:45:33 2024

@author: hacceuee
"""

import subprocess

def check_dependencies():
    try:
        import pandas
        import matplotlib

        # Dependencies are installed
        return True
    except ImportError:
        # Dependencies are not installed
        return False

def install_dependencies():
    print("Required dependencies are not installed.")
    install_choice = input("Do you want to install them now? (y/n): ").lower()
    
    if install_choice == 'y':
        try:
            import subprocess
            subprocess.run(['pip', 'install', '--user', 'pandas', 'matplotlib'], check=True)
            print("Dependencies installed successfully.")
            return True
        except Exception as e:
            print(f"Error installing dependencies: {e}")
            return False
        except subprocess.CalledProcessError:
            print("Error installing dependencies. Please make sure you have pip installed.")
    else:
        print("Please retry the program once you have installed the 'pandas' and 'matplotlib' modules.")
        return False

