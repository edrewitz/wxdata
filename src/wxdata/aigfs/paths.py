"""
This file hosts the function that builds the default AIGFS Directory

(C) Eric J. Drewitz 2025
"""

import os

# Gets Path for Parent Directory
folder = os.getcwd()
folder_modified = folder.replace("\\", "/")

def build_aigfs_directory(type_of_level):
    
    """
    This function builds the AIGFS Data Directory
    
    Required Arguments:
    
    1) type_of_level (String) - The type of level the data is in.
    
        Types of Levels
        ---------------
        
        1) pressure
        2) surface
        
    Optional Arguments: None
    
    Returns
    -------
    
    A directory and the path to that directory for the AIGFS Data files    
    """
    
    type_of_level = type_of_level.upper()
    
    try:
        os.makedirs(f"{folder_modified}/AIGFS/{type_of_level}")
    except Exception as e:
        pass
    
    path = f"{folder_modified}/AIGFS/{type_of_level}"
    
    return path
    
    