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


def clear_idx_files(step=None, model=None, cat=None, paths=None, ens=False):

    """
    This function clears all the .IDX files in a folder.
    """
    
    if ens == False:
        try:
            for item in os.listdir(f"{model}/{cat}/{step}"):
                if item.endswith(".idx"):
                    os.remove(f"{model}/{cat}/{step}/{item}")
        except Exception as e:
            pass
            
    else:
        try:
            for p in paths:
                for item in os.listdir(f"{p}"):
                    if item.endswith(".idx"):
                        os.remove(f"{paths[p]}/{item}")
        except Exception as e:
            pass
        

def ens_folders(model, cat, step, ens_members):
    
    """
    This function builds the directories for ensemble members
    """

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

    paths = []
    for i in range(1, ens_members + 1, 1):
        if os.path.exists(f"{model}/{cat}/{step}/{i}"):
            pass
        else:
            os.mkdir(f"{model}/{cat}/{step}/{i}")

        path = f"{model}/{cat}/{step}/{i}"

        paths.append(path)

    return paths