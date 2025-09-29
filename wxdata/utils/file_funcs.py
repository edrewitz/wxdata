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


