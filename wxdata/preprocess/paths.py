"""
This file hosts the functions that find the various paths to the data files for data pre-processing

(C) Eric J. Drewitz 2025
"""
import os

# Gets Path for Parent Directory
folder = os.getcwd()
folder_modified = folder.replace("\\", "/")

def get_branch_path(model, cat, step):
    
    """
    This function returns the branch path to the data files

    Required Arguments:

    1) model (String) - The forecast model. 

    2) cat (String) - cat (String) - The category of the data. (i.e. mean, control, all members).

    3) step (Integer) - The forecast increment. Either 3, 6 or 12 hour increments.

    Optional Arguments: None

    Returns
    -------

    The branch path of the data files
    """
    model = model.upper()
    cat = cat.upper()

    path = f"{folder_modified}/{model}/{cat}/{step}"
    
    print(path)

    return path
