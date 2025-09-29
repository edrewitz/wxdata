"""
This file hosts functions that download various types of GFS and GEFS Data

(C) Eric J. Drewitz 2025
"""

import urllib.request
import os
import sys
import logging
import glob
import warnings
warnings.filterwarnings('ignore')

from wxdata.gfs.file_funcs import(
    
    build_directory,
    clear_idx_files
    
)
from wxdata.gfs.url_scanners import(
    
    gefs_0p50_url_scanner,
    gefs_0p50_secondary_parameters_url_scanner
)

from wxdata.gfs.process import(
    
    process_gefs0p50_data,
    process_gefs0p50_secondary_parameters_data
    
)

from wxdata.utils.file_scanner import local_file_scanner
from wxdata.utils.recycle_bin import *

def gefs0p50(cat='mean', 
             final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=True):
    
    """
    This function downloads the latest GEFS0P50 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
    
    8) members (List) - Default=[]. The individual ensemble members. There are 30 members in this ensemble.  
    
    
    Returns
    -------
    
    The model runtime and the download URL.     
    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass    
    
    cat = cat.lower()
    
    paths = build_directory('gefs0p50', 
                            cat, 
                            members)

    clear_idx_files('gefs0p50', 
                    cat, 
                    members)
    
    urls, filenames = gefs_0p50_url_scanner(cat, 
                                            final_forecast_hour,
                                            western_bound, 
                                            eastern_bound, 
                                            northern_bound, 
                                            southern_bound, 
                                            proxies, 
                                            step, 
                                            members)
    
    try:
        download = local_file_scanner(paths[-1], 
                                        filenames[-1])
    except Exception as e:
        download = local_file_scanner(paths, 
                                        filenames)       
    
    if download == True:
        print(f"Data is old.\nClearing out old data and downloading new data...")

        try:
            for path in paths:
                for file in os.listdir(f"{path}"):
                    os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        if cat != 'members':
            for path in paths:
                for url, filename in zip(urls, filenames):
                    try:
                        urllib.request.urlretrieve(f"{url}", f"{filename}")
                        os.replace(f"{filename}", f"{path}/{filename}.grib2")
                    except Exception as e:
                        pass
        else:
            start = 0
            increment = int(len(filenames)/len(members))
            stop = increment
            for path in paths:
                for u, f in zip(range(start, stop, 1), range(start, stop, 1)):
                    try:
                        urllib.request.urlretrieve(f"{urls[u]}", f"{filenames[f]}")
                        os.replace(f"{filenames[f]}", f"{path}/{filenames[f]}.grib2")
                    except Exception as e:
                        pass
                start = start + increment
                stop = stop + increment             
                
    else:
        print(f"User has the current dataset.\nSkipping download.")
        
    if process_data == True:
        
        ds = process_gefs0p50_data('gefs0p50', 
                                    cat,
                                    members)
                
        clear_idx_files('gefs0p50', 
                    cat, 
                    members)
        
        return ds
    else:
        pass

def gefs0p50_secondary_parameters(cat='control', 
             final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=True):
    
    """
    This function downloads the latest GEFS0P50 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
    
    8) members (List) - Default=[]. The individual ensemble members. There are 30 members in this ensemble.  
    
    
    Returns
    -------
    
    The model runtime and the download URL.     
    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass     
    
    cat = cat.lower()
    
    paths = build_directory('gefs0p50 secondary parameters', 
                            cat, 
                            members)

    clear_idx_files('gefs0p50 secondary parameters', 
                    cat, 
                    members)
    
    urls, filenames = gefs_0p50_secondary_parameters_url_scanner(cat, 
                                            final_forecast_hour,
                                            western_bound, 
                                            eastern_bound, 
                                            northern_bound, 
                                            southern_bound, 
                                            proxies, 
                                            step, 
                                            members)
    
    try:
        download = local_file_scanner(paths[-1], 
                                        filenames[-1])
    except Exception as e:
        download = local_file_scanner(paths, 
                                        filenames)       
    
    if download == True:
        print(f"Data is old.\nClearing out old data and downloading new data...")

        try:
            for path in paths:
                for file in os.listdir(f"{path}"):
                    os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        if cat != 'members':
            for path in paths:
                for url, filename in zip(urls, filenames):
                    try:
                        urllib.request.urlretrieve(f"{url}", f"{filename}")
                        os.replace(f"{filename}", f"{path}/{filename}.grib2")
                    except Exception as e:
                        pass
        else:
            start = 0
            increment = int(len(filenames)/len(members))
            stop = increment
            for path in paths:
                for u, f in zip(range(start, stop, 1), range(start, stop, 1)):
                    try:
                        urllib.request.urlretrieve(f"{urls[u]}", f"{filenames[f]}")
                        os.replace(f"{filenames[f]}", f"{path}/{filenames[f]}.grib2")
                    except Exception as e:
                        pass
                start = start + increment
                stop = stop + increment             
                
    else:
        print(f"User has the current dataset.\nSkipping download.")
    
    if process_data == True:
        
        ds = process_gefs0p50_secondary_parameters_data('gefs0p50 secondary parameters', 
                                    cat,
                                    members)
                
        clear_idx_files('gefs0p50 secondary parameters', 
                    cat, 
                    members)
        
        return ds
    else:
        pass