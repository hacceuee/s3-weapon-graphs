# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 01:07:20 2024

@author: hacceuee
"""

import os
import re
import json

script_directory = os.path.dirname(os.path.abspath(__file__))
ideal_file_path = os.path.join(script_directory, "data.json")


#------------------WRITES DATA FILE TO LOCAL JSON
def copy_file_locally(data):
    
    with open(ideal_file_path, 'w', encoding='utf-8') as file:
        file.write(data)
        
def check_for_file(): 
    # Check if data.json exists in the same directory
    file_path = ideal_file_path
    
    if os.path.exists(file_path):        
        # Correct file
        if correct_file(file_path):
            return file_path
    
    return None

def correct_file(file_path):
    # Open file and modify it
    with open(file_path, encoding="utf8") as file:
        data = file.read()
    
    # Check first character for '['
    if data.strip().startswith('['):
        if file_path != ideal_file_path: # Copy file locally if it doesn't exist there 
            copy_file_locally(data)
        
    else:    # Modify file
        data = re.sub(r'}}\s*{"id":', '}},\n{"id":', data) # Add a comma between '}}' and '{"id":' 
        data = "[" + data + "]" # Add a starting '[' and ending ']'
        copy_file_locally(data)

    try:
        # Attempt to open the modified file and parse it as JSON
        with open(ideal_file_path, encoding="utf8") as file:
            json.load(file)
        return True
    except json.JSONDecodeError:
        return False

def import_new_file(file_path):
    #------------------CORRECTING FILE
    
    if correct_file(file_path):
        return ideal_file_path
    
    return None