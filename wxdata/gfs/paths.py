"""
This file hosts the functions that find the various paths to the data files for data pre-processing

(C) Eric J. Drewitz 2025
"""
import os

# Gets Path for Parent Directory
folder = os.getcwd()
folder_modified = folder.replace("\\", "/")

def gefs_branch_path(model, 
                         cat,
                         members):
    
    """
    This function returns the branch path to the data files

    Required Arguments:

    1) model (String) - The forecast model. 

    2) cat (String) - cat (String) - The category of the data. (i.e. mean, control, all members).
    
    3) members (List) - The individual ensemble members. There are 30 members in this ensemble. 

    Optional Arguments: None

    Returns
    -------

    The branch path of the data files
    """
    model = model.upper()
    cat = cat.upper()
    
    if cat == 'MEMBERS':
        paths = []
        for member in members:
            path = f"{model}/{cat}/{member}"
            paths.append(path)
    else:
        paths = f"{model}/{cat}"
    
    return paths