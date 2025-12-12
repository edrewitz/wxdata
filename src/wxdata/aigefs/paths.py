"""
This file hosts the functions that build the directory for the AIGEFS.

(C) Eric J. Drewitz 2025
"""

import os

# Gets Path for Parent Directory
folder = os.getcwd()
folder_modified = folder.replace("\\", "/")

def build_aigefs_directory(param_type,
                           members):
    
    """
    This function builds the default directory for the AIGEFS.
    
    Required Arguments:
    
    1) param_type (String) - The type of parameters
    
    Parameter Types
    ---------------
    
    1) pressure
    2) surface
    
    2) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.
    
    Returns
    -------
    
    The AIGEFS Directory and the paths associated with the AIGEFS Directory.   
    """
    
    paths = []
    for member in members:
        path = f"{folder_modified}/AIGEFS/{param_type.upper()}/{member}"
        paths.append(path)
        
        try:
            os.makedirs(f"{folder_modified}/AIGEFS/{param_type.upper()}/{member}")
        except Exception as e:
            pass
        
    return paths
            