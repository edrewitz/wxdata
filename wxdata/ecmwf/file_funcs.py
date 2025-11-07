"""
This file hosts the functions that build and manage the branch of the ECMWF data directory.

(C) Eric J. Drewitz 2025
"""

import os
from datetime import datetime

def build_directory(model, cat):
    
    """
    This function checks if the necessary branch to the directory exists and if not, it will build it. 
    
    Required Arguments:
    
    1) model (String) - The model being used. 
    
    Models
    ------
    1) ifs
    2) aifs
    
    2) cat (String) - The category of the model data. 
    
    Categories
    ----------
    
    1) operational
    2) high res
    3) wave
    
    Returns
    -------
    
    Builds directory branch if needed.
    """
    
    model = model.upper()
    cat = cat.upper()
    
    if os.path.exists(f"ECMWF"):
        pass
    else:
        os.mkdir(f"ECMWF")
    
    if os.path.exists(f"ECMWF/{model}"):
        pass
    else:
        os.mkdir(f"ECMWF/{model}")
        
    if os.path.exists(f"ECMWF/{model}/{cat}"):
        pass
    else:
        os.mkdir(f"ECMWF/{model}/{cat}")
        

def clear_idx_files(path):
    
    """
    This function clears all the .idx files in a directory
    """
    
    try:
        for file in os.listdir(f"{path}"):
            if file.endswith(".idx"):
                os.remove(f"{path}/{file}")
            else:
                pass
    except Exception as e:
        pass
    
def clear_old_data(path):
    
    """
    This function clears old data in a specified path.     
    """
    
    try:
        for file in os.listdir(f"{path}"):
            os.remove(f"{path}/{file}")
    except Exception as e:
        pass
    
    
def parse_filename(filename):
    
    """
    This function parses the filename for the correct date/time
    
    Required Arguments:
    
    1) filename (String) - The filename.
    
    Optional Arguments: None
    
    Returns
    -------
    
    A datetime object with the date/time from the filename.     
    """
    
    year = int(f"{filename[0]}{filename[1]}{filename[2]}{filename[3]}")
    month = int(f"{filename[4]}{filename[5]}")
    day = int(f"{filename[6]}{filename[7]}")
    hour = int(f"{filename[8]}{filename[9]}")
    
    date = datetime(year, month, day, hour)
    
    return date