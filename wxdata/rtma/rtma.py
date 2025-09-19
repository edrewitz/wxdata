"""
This file hosts the function that downloads and returns RTMA Data from the NCEP/NOMADS Server. 

(C) Eric J. Drewitz 2025
"""
import urllib.request
import os
import sys
import logging
import glob
import warnings
import time
warnings.filterwarnings('ignore')

from wxdata.scanners.url_scanners import rtma_url_scanner
from wxdata.scanners.file_scanners import rtma_file_scanner

from wxdata.utils.file_funcs import clear_idx_files
from wxdata.rtma.file_funcs import build_rtma_directory
from wxdata.rtma.process import process_data

from wxdata.utils.recycle_bin import *
clear_recycle_bin_windows()
clear_trash_bin_mac()
clear_trash_bin_linux()

def rtma(model='rtma', cat='analysis', proxies=None):
    
    """
    This function downloads the latest RTMA Dataset and returns it as an xarray data array. 
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) 
    """
    
    model = model.upper()
    cat = cat.upper()
    
    url, fname = rtma_url_scanner(model, cat, proxies)
    
    path = build_rtma_directory(model, cat)
    clear_idx_files(model=model, paths=path)
    download = rtma_file_scanner(path, fname, model)
    
    if download == True:
        print("Deleting old data and downloading the new data.")
        try:
            for file in os.listdir(f"{path}"):
                os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        urllib.request.urlretrieve(f"{url}{fname}", f"{fname}")
    
        os.replace(f"{fname}", f"{path}/{fname}")

    else:
        print("Data in directory is up to date. Skipping download.")
    
    ds = process_data(path, fname, model)
    clear_idx_files(model=model, paths=path)
    
    return ds
    
    
    