# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 01:07:20 2024

@author: hacceuee
"""

import os
import re

def check_for_file(): 
    print("/n------FILE EVALUATION/n")
    # Check if data.json exists in the same directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, "data.json")
    
    # Ask for file path if not found
    if os.path.exists(file_path):
        user_file_path = file_path
    else: 
        print(f"File not found: {file_path}")
        user_file_path = input("Enter the absolute path to the data.json file downloaded from the Export (Splatoon 3) (JSON (stat.ink format, gzipped)) on your profile on stat.ink. It should be unzipped: ")
    
    # Open file
    with open(user_file_path, encoding="utf8") as file:
        data = file.read()
        
    # Check first character for '['
    if data.strip().startswith('['):
        print("File successfully parsed")
        #check to make sure the file exists, if it doesn't, make a copy
        return file_path
        
    # Modify file
    data = re.sub(r'}}\s*{"id":', '}},\n{"id":', data) # Add a comma between '}}' and '{"id":' 
    data = "[" + data + "]" # Add a starting '[' and ending ']'
        
    # Write file to local .json if modified or new
    with open(file_path, 'w',encoding='utf-8') as file:
        file.write(data)
    print("File has been modified or moved")
    return file_path

#TODO: santize input, add option for updating stored file