"""
This file hosts the functions that do the following:

1) Build directories for ensemble member data files. 

2) Clear IDX files

3) Unzip files

(C) Eric J. Drewitz 2025
"""


import os
import gzip

def extract_gzipped_file(compressed_file, decompressed_file):
    
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


def clear_idx_files(directory=None, step=None, model=None, cat=None, paths=None, ens=False):

    """
    This function clears all the .IDX files in a folder.
    """
    model = model.upper()
    
    if model == 'GEFS0P50' or model == 'GEFS0P50 SECONDARY PARAMETERS' or model == 'GEFS0P25':
        if directory != None:
            directory = directory.upper()
        
        if ens == False:
            try:
                for item in os.listdir(f"{model}/{cat}/{step}/{directory}"):
                    if item.endswith(".idx"):
                        os.remove(f"{model}/{cat}/{step}/{directory}/{item}")
            except Exception as e:
                pass
                
        else:
            try:
                for p in paths:
                    for item in os.listdir(f"{p}"):
                        if item.endswith(".idx"):
                            os.remove(f"{p}/{item}")
            except Exception as e:
                pass
        
    elif model == 'RTMA' or model == 'AK RTMA' or model == 'HI RTMA' or model == 'GU RTMA':
        path = paths
        try:
            for item in os.listdir(f"{path}"):
                if item.endswith(".idx"):
                    os.remove(f"{path}/{item}")
        except Exception as e:
            pass
        
    else:
        pass

def ens_folders(model, cat, step, directory, ens_members):
    
    """
    This function builds the directories for ensemble members
    """
    directory = directory.upper()
    
    if os.path.exists(f"{model}"):
        pass
    else:
        os.mkdir(f"{model}")

    if os.path.exists(f"{model}/{cat}"):
        pass
    else:
        os.mkdir(f"{model}/{cat}")

    if os.path.exists(f"{model}/{cat}/{step}"):
        pass
    else:
        os.mkdir(f"{model}/{cat}/{step}")
        
    if os.path.exists(f"{model}/{cat}/{step}/{directory}"):
        pass
    else:
        os.mkdir(f"{model}/{cat}/{step}/{directory}")

    paths = []
    for i in ens_members:
        if os.path.exists(f"{model}/{cat}/{step}/{directory}/{i}"):
            pass
        else:
            os.mkdir(f"{model}/{cat}/{step}/{directory}/{i}")

        path = f"{model}/{cat}/{step}/{directory}/{i}"

        paths.append(path)

    return paths