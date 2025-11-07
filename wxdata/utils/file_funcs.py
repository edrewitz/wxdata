"""
This file hosts the functions that do the following:

1) Build directories for ensemble member data files. 

2) Clear IDX files

3) Unzip files

(C) Eric J. Drewitz 2025
"""


import os
import gzip

def extract_gzipped_file(compressed_file, 
                         decompressed_file):
    
    """
    Extracts a gzipped file to a specified location.

    Parameters:
    compressed_file (str): Path to the gzipped file.
    decompressed_file (str): Path where the decompressed file will be saved.
    """

    with gzip.open(compressed_file, 'rb') as f_in:
        with open(decompressed_file, 'wb') as f_out:
            f_out.write(f_in.read())
            
    if os.path.exists(compressed_file):
        os.remove(compressed_file)
    else:
        pass
    

def file_paths_for_xarray(paths):
    
    """
    This function returns the file paths for xarray.open_mfdataset(paths)
    
    Required Arguments:
    
    1) path (String) - The file path. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    A list of complete file paths for xarray.open_mfdataset(paths)   
    """
    new_paths = []
    if len(paths) > 1:
        for path in paths:
            files = []
            new_paths.append(files)
            for file in os.listdir(f"{path}"):
                f = f"{path}/{file}"
                files.append(f)

    else:
        for file in os.listdir(f"{paths[0]}"):
            p = f"{paths[0]}/{file}"
            new_paths.append(p)
        
    return new_paths

def clear_gefs_idx_files(paths):
    
    """
    This function clears all GEFS .IDX files in a user's specified directory   
    """
    if len(paths) > 1:
        try:
            for path in paths:
                for file in os.listdir(f"{path}"):
                    if file.endswith(".idx"):
                        os.remove(f"{path}/{file}")
                    else:
                        pass
        except Exception as e:
            pass
        
    else:
        try:
            for file in os.listdir(f"{paths[0]}"):
                if file.endswith(".idx"):
                    os.remove(f"{paths[0]}/{file}")
                else:
                    pass
        except Exception as e:
            pass
                
def clear_ecmwf_idx_files(path):
    
    """
    This function clears all ECMWF .IDX files. 
    """
    
    try:
        for file in os.listdir(f"{path}"):
            if file.endswith(".idx"):
                os.remove(f"{path}/{file}")
            else:
                pass
    except Exception as e:
        pass
                

def clear_rtma_idx_files(directory):
    
    """
    This function clears all RTMA .IDX files. 
    """
    
    try:
        for file in os.listdir(f"{directory}"):
            if file.endswith(".idx"):
                os.remove(f"{directory}/{file}")
            else:
                pass
    except Exception as e:
        pass
            
            
def custom_branch(path):
    
    """
    This function will allow users to save files to a custom path if they do not wish to use
    the pre-built directory. This could also be useful for users with existing directories
    from current and previous processes. 
    
    Required Arguments:
    
    1) path (String) - The full path to where the data files will be saved. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    A directory branch path specified by the user.   
    The path of that directory.    
    """
    
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
        
    return path
        
def custom_branches(paths):
    
    """
    This function will allow users to save files to a set of custom paths if they do not wish to use
    the pre-built directory. This could also be useful for users with existing directories
    from current and previous processes. This is to be used for users who wish to download
    ensemble data and bin their ensemble data into seperate folders by ensemble member. 
    
    Required Arguments:
    
    1) paths (String List) - The a list of paths specified by the user. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    A directory branch path list specified by the user.   
    The paths of that directory.    
    """
    
    for path in paths:
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        except Exception as e:
            print(f"An error occurred: {e}")
        
    return paths
        
        
        