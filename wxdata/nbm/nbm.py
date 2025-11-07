"""
This file hosts the functions the user interacts with to download NBM data.

(C) Eric J. Drewitz
"""

import wxdata.client.client as client
import sys
import warnings
import os
import time
warnings.filterwarnings('ignore')

from wxdata.nbm.paths import build_directory
from wxdata.nbm.url_scanner import nbm_url_scanner
from wxdata.utils.file_scanner import local_file_scanner
from wxdata.utils.recycle_bin import *


def national_blend_of_models(region='conus',
                            custom_directory='default',
                            proxies=None,
                            clear_recycle_bin=True,
                            chunk_size=8192,
                            notifications='off'):
    
    
    """
    This function downloads the latest NBM data and saves the files to a folder.
    
    The user can specify a folder by changing custom_directory=path.
    
    If the user does not specify their own path, a path of f:NBM/{region} will be created by default.
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) region (String) - The region identifier.
    
        Regions
        -------
        
        'conus'
        'ak'
        'hi'
        'pr'
        'gu'
        
    2) custom_directory (String or None) - Default=None. When set to None, the default directory is used.
    
    3) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
                        
    Returns
    -------
    
    Latest NBM run saved to the specified folder.    
    """
    
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    
    path = build_directory(region,
                           custom_directory)
    
    url, files, run = nbm_url_scanner(proxies,
                                 region)
    
    filename = files[-1]
    download = local_file_scanner(path,
                                  filename,
                                  'nomads',
                                  run)
    
    if download == True:
        
        try:
            for file in os.listdir(f"{path}"):
                os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        print(f"Downloading...")

        for f in files:
            client.get_gridded_data(f"{url}",
                        path,
                        f"{f}.grib2",
                        proxies=proxies,
                        chunk_size=chunk_size,
                        notifications=notifications)  
            
        print(f"Download Complete.")
    else:
        print(f"User has latest data. Skipping download.")
                            

                        
                