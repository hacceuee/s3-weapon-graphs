# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 01:07:20 2024

@author: hacceuee
"""

import os
import re
import json

#------------------WRITES DATA FILE TO LOCAL JSON
def copy_file_locally(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)
    print(f"File has successfully been parsed and copied to {file_path}")
        
def check_for_file(): 
    print("\n------FILE EVALUATION\n")
    # Check if data.json exists in the same directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, "data.json")
    
    # Ask the user whether to continue with the loaded file, or preparing to ask for a new file path
    if os.path.exists(file_path):
        user_file_path = file_path
        # Ask the user whether to continue with the loaded file
        user_input = input("JSON found. Continue with this file? (y/n) or press enter to continue with the loaded file: ").lower()
    
        if user_input == 'n':
            # If the user enters 'n', set user_file_path to None
            user_file_path = None
    else:
        # Ask for file path if not found
        user_file_path = None

        
    while True: # File validation loop
        
        # Ask for file path of file to parse
        if user_file_path is None:
            print(f"\nFile not found: {file_path}")
            user_file_path = input("\nEnter the absolute path to the data.json file downloaded from the Export (Splatoon 3) (JSON (stat.ink format, gzipped)) on your profile on stat.ink. It should be unzipped: ")
            # Remove leading and trailing quotes and spaces from the user_file_path
            user_file_path = user_file_path.strip().strip('"')
        
        #------------------CORRECTING FILE
        
        # Open file and modify it
        with open(user_file_path, encoding="utf8") as file:
            data = file.read()
        
        # Check first character for '['
        if data.strip().startswith('['):
            if not os.path.exists(file_path): # Copy file locally if it doesn't exist there 
                copy_file_locally(file_path, data)
            print("\nFile successfully parsed. Please wait while the games are processed.")
            
        else:    # Modify file
            data = re.sub(r'}}\s*{"id":', '}},\n{"id":', data) # Add a comma between '}}' and '{"id":' 
            data = "[" + data + "]" # Add a starting '[' and ending ']'
            copy_file_locally(file_path, data)

        try:
            # Attempt to open the modified file and parse it as JSON
            with open(file_path, encoding="utf8") as file:
                json.load(file)
            break  # If successful, break out of the loop
        except json.JSONDecodeError:
            print("Invalid JSON file. Please provide a valid JSON file.")
            user_file_path = None  # Reset user_file_path to trigger asking for a new path in the next iteration

    return file_path