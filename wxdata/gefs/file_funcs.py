"""
This file hosts the function that builds the directory and directory branches

(C) Eric J. Drewitz 2025
"""

import os

def build_directory(model, cat, members):
    
    """
    This function builds the directory for the GFS/GEFS data files.
    
    Required Arguments:
    
    1) model (String) - The type of GFS/GEFS model being used. 
    
    2) cat (String) - The category of the data. 
    
    3) members (List) - A list of ensemble members if the user wants the individual members. 
    
    Returns
    -------
    
    A new directory/directory branch if it was not created before.  
    The paths of the directory branches   
    """
    model = model.upper()
    cat = cat.upper()
    
    paths = []
    
    if os.path.exists(f"{model}"):
        pass
    else:
        os.mkdir(f"{model}")
        
    if os.path.exists(f"{model}/{cat}"):
        pass
    else:
        os.mkdir(f"{model}/{cat}")
        
    if cat == 'MEMBERS':
        for member in members:
            if os.path.exists(f"{model}/{cat}/{member}"):
                pass
            else:
                os.mkdir(f"{model}/{cat}/{member}")
                
            path = f"{model}/{cat}/{member}"
            paths.append(path)
    else:
        path = f"{model}/{cat}"
        paths.append(path)
        
    return paths

def clear_idx_files(model, cat, members):
    
    """
    This function clears all the .IDX files in a folder. 
    
    Required Arguments:
    
    
    Optional Arguments:
    
    Returns
    -------
    
    """
    model = model.upper()
    cat = cat.upper()
    
    if cat != 'MEMBERS':
        path = f"{model}/{cat}"
        try:
            for file in os.listdir(f"{path}"):
                if file.endswith(".idx"):
                    os.remove(f"{path}/{file}")
        except Exception as e:
            pass
    
    else:
        paths = []
        for member in members:
            path = f"{model}/{cat}/{member}"
            paths.append(path)
            
        try:
            for path in paths:
                for file in os.listdir(f"{path}"):
                    if file.endswith(".idx"):
                        os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
            
def clear_empty_files(paths):
    
    """
    This file checks for empty files in the directory and clears them if they exist. 
    
    Required Arguments:
    
    1) paths (List) - The list of file paths.  
    
    Optional Arguments: None
    
    Returns
    -------
    
    Clears out empty files. Some variables do not have a 0th forecast hour. 
    """                    
    try:
        for path in paths:
            for file in os.listdir(f"{path}"):
                size = os.path.getsize(f"{path}/{file}")
                if size == 0:
                    os.remove(f"{path}/{file}")
                else:
                    pass
    except Exception as e:
        pass
        
    
    