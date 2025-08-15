"""
This module has the functions that download, unzip and return METAR data. 

(C) Eric J. Drewitz 2025
"""

import pandas as pd
import csv
import urllib.request
import os

from wxdata.utils.file_funcs import extract_gzipped_file
from wxdata.utils.recycle_bin import *
clear_recycle_bin_windows()
clear_trash_bin_mac()
clear_trash_bin_linux()

def download_metar_data():
    
    """
    Downloads the latest METAR Data from NOAA/AWC and returns a Pandas DataFrame.

    Returns:        
    pd.DataFrame: A DataFrame containing the METAR data.
    """
    
    urllib.request.urlretrieve(f"https://aviationweather.gov/data/cache/metars.cache.csv.gz", f"metars.cache.csv.gz")
    extract_gzipped_file('metars.cache.csv.gz', 'metars.csv')
    
    if os.path.exists(f"METAR Data"):
        pass
    else:
        os.mkdir(f"METAR Data")

    try:
        for file in os.listdir(f"METAR Data"):
            os.remove(f"METAR Data/{file}")
    except Exception as e:
        pass
        
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