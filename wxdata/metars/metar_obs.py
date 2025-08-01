"""
This module has the functions that download, unzip and return METAR data. 

(C) Eric J. Drewitz 2025
"""

import pandas as pd
import csv
import urllib.request
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

def download_metar_data():
    
    """
    Downloads the latest METAR Data from NOAA/AWC and returns a Pandas DataFrame.

    Returns:        
    pd.DataFrame: A DataFrame containing the METAR data.
    """
    extract_gzipped_file('metars.cache.csv.gz', 'metars.csv')
    
    if os.path.exists(f"METAR Data"):
        pass
    else:
        os.mkdir(f"METAR Data")
        
    os.replace(f"metars.csv", f"METAR Data/metars.csv")

    with open('METAR Data/metars.csv', 'r', newline='') as csvfile:
        # Create a reader object
        csv_reader = csv.reader(csvfile)
        rows = []
        for row in csv_reader:
            rows.append(row)
    
    data = []
    for i in range(0, len(rows), 1):
        if i > 4:
            data.append(rows[i])
            
    df = pd.DataFrame(data)
    
    new_column_names = df.iloc[0].tolist()
    
    df.columns = new_column_names
    
    df = df.drop('raw_text', axis=1)
    
    df = df.drop(index=0)
    
    return df