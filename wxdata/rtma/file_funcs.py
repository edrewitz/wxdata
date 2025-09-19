"""
This file hosts the functions that build the RTMA Data Directory

(C) Eric J. Drewitz 2025
"""

import os

def build_rtma_directory(model, cat):
    
    
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