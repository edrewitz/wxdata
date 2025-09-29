"""
This file hosts the functions that build the RTMA Data Directory

(C) Eric J. Drewitz 2025
"""

import os

def build_directory(model, 
                    cat):
    
    
    """
    This function builds the directory for the RTMA Data
    
    Required Arguments:
    
    1) model (String) - The RTMA model being used. 
    
    2) cat (String) - The category of the data. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    A directory and path to the data.     
    """
    model = model.upper()
    cat = cat.upper()
    
    if os.path.exists(f"{model}"):
        pass
    else:
        os.mkdir(f"{model}")
        
    if os.path.exists(f"{model}/{cat}"):
        pass
    else:
        os.mkdir(f"{model}/{cat}")
        
    path = f"{model}/{cat}"
    
    return path

def clear_idx_files(path):
    
    """
    This function clears all the .IDX files in a folder. 
    
    Required Arguments:
    
    
    Optional Arguments:
    
    Returns
    -------
    
    """
    try:
        for file in os.listdir(f"{path}"):
            if file.endswith(".idx"):
                os.remove(f"{path}/{file}")
    except Exception as e:
        pass
    