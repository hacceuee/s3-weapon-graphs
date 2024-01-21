# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 11:45:33 2024

@author: hacceuee
"""

import subprocess

def install_dependencies():
    try:
        subprocess.check_call(['pip', 'install', '--user', 'pandas', 'matplotlib'])
    except subprocess.CalledProcessError:
        print("Error installing dependencies. Please make sure you have pip installed.")
