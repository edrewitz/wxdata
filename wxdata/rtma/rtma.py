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

def bounds(model):
    
    """
    This function determines the boundaries for the data based on the region.
    
    Required Arguments: 
    
    1) model (String) - The RTMA model being used. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    The bounding box for the data.     
    """
    
    models = {
        
        'RTMA':[-125, -65, 20, 50],
        'HI RTMA':[-180, 180, -90, 90],
        'PR RTMA':[-68, -65, 17, 19],
        'GU RTMA':[-180, 180, -90, 90],
        'AK RTMA':[-180, -120, 45, 75]
        
    }
    
    return models[model][0], models[model][1], models[model][2], models[model][3]

def rtma(model='rtma', 
         cat='analysis', 
         proxies=None,
         process_data=True,
         clear_recycle_bin=True,
         western_bound=None,
         eastern_bound=None,
         southern_bound=None,
         northern_bound=None):
    
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
                        
    4) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    5) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    6) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    7) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    8) southern_bound (Float or Integer) - Default=-90. The northern bound of the data needed.

    9) northern_bound (Float or Integer) - Default=90. The southern bound of the data needed.
    
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
    
    if western_bound == None and eastern_bound == None and southern_bound == None and northern_bound == None:
        western_bound, eastern_bound, southern_bound, northern_bound = bounds(model)
    else:
        western_bound = western_bound
        eastern_bound = eastern_bound 
        southern_bound = southern_bound 
        northern_bound = northern_bound
    
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
        
    

    
    
    