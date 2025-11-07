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

def sorted_paths(folder_path, ascending=True):
    """
    Sorts files in a given folder by their modification date.

    Args:
        folder_path (str): The path to the folder containing the files.
        ascending (bool): If True, sorts in ascending order (oldest first).
                          If False, sorts in descending order (newest first).

    Returns:
        list: A list of file paths sorted by modification date.
    """
    try:
        # Get a list of all files (not directories) in the specified folder
        files = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ]

        # Sort the files based on their modification time
        # os.path.getmtime() returns the modification time as a float (seconds since epoch)
        sorted_files = sorted(files, key=os.path.getmtime, reverse=not ascending)
        return sorted_files
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []