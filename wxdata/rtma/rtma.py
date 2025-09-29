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

from wxdata.rtma.file_funcs import(
     build_directory,
     clear_idx_files
)

from wxdata.rtma.url_scanners import rtma_url_scanner
from wxdata.utils.file_scanner import local_file_scanner
from wxdata.rtma.process import process_rtma_data
from wxdata.utils.recycle_bin import *

def rtma(model='rtma', 
         cat='analysis', 
         western_bound=-125,
         eastern_bound=-65,
         northern_bound=50,
         southern_bound=20,
         proxies=None,
         process_data=True,
         clear_recycle_bin=True):
    
    """
    This function downloads the latest RTMA Dataset and returns it as an xarray data array. 
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) model (String) - Default='rtma'. The RTMA model being used:
    
    RTMA Models
    -----------
    
    CONUS = 'rtma'
    Alaska = 'ak rtma'
    Hawaii = 'hi rtma'
    Puerto Rico = 'pr rtma'
    Guam = 'gu rtma'
    
    2) cat (String) - Default='analysis'. The category of the RTMA dataset. 
    
    RTMA Categories
    ---------------
    
    analysis - Latest RTMA Analysis
    error - Latest RTMA Error
    surface 1 hour forecast - RTMA Surface 1 Hour Forecast
    
    3) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                        }
    
    Returns
    -------
    
    An xarray data array of the RTMA Dataset with variable keys converted from the GRIB format to a Plain Language format. 
    
    Variable Keys
    -------------
    
    'orography'
    'surface_pressure'
    '2m_temperature'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_specific_humidity'
    'surface_visibility'
    'cloud_ceiling_height'
    'total_cloud_cover'
    '10m_u_wind_component'
    '10m_v_wind_component'
    '10m_wind_direction'
    '10m_wind_speed'
    '10m_wind_gust'
    
    """
    
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    
    model = model.upper()
    cat = cat.upper()
    
    path = build_directory(model,
                           cat)
    
    clear_idx_files(path)
    
    url, filename = rtma_url_scanner(model, 
                    cat,
                    western_bound, 
                    eastern_bound, 
                    northern_bound, 
                    southern_bound, 
                    proxies)
    
    download = local_file_scanner(path, 
                                filename) 
    
    if download == True:
        print(f"{model} Data is old. Please Wait - Updating...")
        urllib.request.urlretrieve(f"{url}", f"{filename}")
        os.replace(f"{filename}", f"{path}/{filename}.grib2")
    else:
        print(f"{model} Data is current. Skipping download.")
        
    if process_data == True:
        filename = f"{filename}.grib2"
        ds = process_rtma_data(path, 
                                filename, 
                                model)

        clear_idx_files(path)
        
        return ds
    
    else:
        pass
        
    

    
    
    