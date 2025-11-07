"""
This file has the functions that manage the NBM directory.

(C) Eric J. Drewitz 2025
"""

import os

def build_directory(region,
                    custom_directory):
    
    """
    This function builds the directory for the NBM data.
    
    Required Arguments: 
    
    1) region (String) - The NBM region. 
    
    2) custom_directory (String) - Default='default'. When set to 'default', the automatic directory wxdata builds and manages will be used.
    For users who wish to use their own directory path, set custom_directory=path.
    
    Optional Arguments: None
    
    Returns
    -------
    
    A directory for the NBM data.     
    """
    region = region.upper()
    
    if custom_directory == 'default':
        path = f"NBM/{region}"
        try:
            os.makedirs(f"NBM/{region}")
        except Exception as e:
            pass
        
    else:
        path = custom_directory
        try:
            os.makedirs(f"{custom_directory}")
        except Exception as e:
            pass
        
    return path