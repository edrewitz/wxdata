"""
This file hosts the functions that find the various paths to the ECMWF data files for data pre-processing

(C) Eric J. Drewitz 2025
"""
import os

# Gets Path for Parent Directory
folder = os.getcwd()
folder_modified = folder.replace("\\", "/")

def ecmwf_branch_paths(model, cat):
    
    """
    This function returns the branch path the ECMWF files are saved in. 
    
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
    
    The branch path of the ECMWF data files.
    """
    
    model = model.upper()
    cat = cat.upper()
    
    path = f"ECMWF/{model}/{cat}"
    
    return path

