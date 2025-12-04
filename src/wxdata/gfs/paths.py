"""
This file hosts the functions that find the various paths to the GFS data files for data pre-processing

(C) Eric J. Drewitz 2025
"""
import os

# Gets Path for Parent Directory
folder = os.getcwd()
folder_modified = folder.replace("\\", "/")

def build_directory(model, 
                    cat):
    
    """
    This function builds the directory for the GFS data and returns the path. 
    
    1) model (String) - The GFS model being used.
    
    Valid categories
    ----------------
    
    1) GFS0P25
    2) GFS0P25 SECONDARY PARAMETERS
    3) GFS0P50
    
    2) cat (string) - The category of data. 
    
    Valid categories
    -----------------
    
    1) atmosphere
    2) ocean
    
    Returns
    -------
    
    The path of the GFS directory    
    """
    
    model = model.upper()
    cat = cat.upper()
    
    try:
        os.makedirs(f"{folder_modified}/{model}/{cat}")
    except Exception as e:
        pass
    
    path = f"{folder_modified}/{model}/{cat}/"
    
    return path
