"""
This file hosts functions that download GEM Global and GEM Ensemble Data

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

from wxdata.scanners.url_scanners import gem_global_scanner
#from wxdata.scanners.file_scanners import file_scanner

from wxdata.gem.file_funcs import(
    
    gem_global_file_prefixes,
    build_gem_global_directory,
    parameter_list
)

from wxdata.utils.file_funcs import(
    
    ens_folders, 
    clear_idx_files    
)

#from wxdata.gem.process import process_data

from wxdata.utils.recycle_bin import *
clear_recycle_bin_windows()
clear_trash_bin_mac()
clear_trash_bin_linux()


def gem_global(western_bound=-180, eastern_bound=180, northern_bound=90, southern_bound=-90, set='full', final_forecast_hour=240, step=3, proxies=None):
    
    """
    This function downloads the GEM Global data and returns the complete dataset as an xarray data array.
    
    """
    
    if final_forecast_hour > 240:
        final_forecast_hour = 240
    else:
        final_forecast_hour = final_forecast_hour
        
    stop = final_forecast_hour + step
    
    url, run, date = gem_global_scanner(final_forecast_hour, proxies)
    
    file_prefixes = gem_global_file_prefixes(run, date, set)
    
    build_gem_global_directory(set)
    
    parameters = parameter_list(set)
    
    error = False
    max_retries = 3
    
    for f, p in zip(file_prefixes, parameters):
        for i in range(0, stop, step):
            if i < 10:
                retry = 0
                try:
                    urllib.request.urlretrieve(f"{url}00{i}/{f}_P00{i}.grib2", f"{f}_P00{i}.grib2")
                    os.replace(f"{f}_P00{i}.grib2", f"GEM GLOBAL/{p}/{f}_P00{i}.grib2")
                    error = False
                except Exception as e:
                    error = True
                    print(f"Temporarily lost connection to server. Waiting 30 seconds and then trying again to reconnect and resume.")
                    time.sleep(30)
                    retry = retry + 1
                    while error == True:
                        if retry > max_retries:
                            print("Unable to reconnect...Exiting...")
                            sys.exit(1)
                        else: 
                            try:
                                urllib.request.urlretrieve(f"{url}00{i}/{f}_P00{i}.grib2", f"{f}_P00{i}.grib2")
                                os.replace(f"{f}_P00{i}.grib2", f"GEM GLOBAL/{p}/{f}_P00{i}.grib2")
                                error = False
                            except Exception as e:
                                error = True
                                print(f"Temporarily lost connection to server. Waiting 30 seconds and then trying again to reconnect and resume.")
                                time.sleep(30)
                                retry = retry + 1
                    
            elif i >= 10 and i < 100:
                retry = 0
                try:
                    urllib.request.urlretrieve(f"{url}0{i}/{f}_P0{i}.grib2", f"{f}_P0{i}.grib2")
                    os.replace(f"{f}_P0{i}.grib2", f"GEM GLOBAL/{p}/{f}_P0{i}.grib2")
                    error = False
                except Exception as e:
                    error = True
                    print(f"Temporarily lost connection to server. Waiting 30 seconds and then trying again to reconnect and resume.")
                    time.sleep(30)
                    retry = retry + 1
                    while error == True:
                        if retry > max_retries:
                            print("Unable to reconnect...Exiting...")
                            sys.exit(1)
                        else: 
                            try:
                                urllib.request.urlretrieve(f"{url}0{i}/{f}_P0{i}.grib2", f"{f}_P0{i}.grib2")
                                os.replace(f"{f}_P0{i}.grib2", f"GEM GLOBAL/{p}/{f}_P0{i}.grib2")
                                error = False
                            except Exception as e:
                                error = True
                                print(f"Temporarily lost connection to server. Waiting 30 seconds and then trying again to reconnect and resume.")
                                time.sleep(30)
                                retry = retry + 1
            else:
                retry = 0
                try:
                    urllib.request.urlretrieve(f"{url}{i}/{f}_P{i}.grib2", f"{f}_P{i}.grib2")
                    os.replace(f"{f}_P{i}.grib2", f"GEM GLOBAL/{p}/{f}_P{i}.grib2")
                    error = False
                except Exception as e:
                    error = True
                    print(f"Temporarily lost connection to server. Waiting 30 seconds and then trying again to reconnect and resume.")
                    time.sleep(30)
                    retry = retry + 1
                    while error == True:
                        if retry > max_retries:
                            print("Unable to reconnect...Exiting...")
                            sys.exit(1)
                        else: 
                            try:
                                urllib.request.urlretrieve(f"{url}{i}/{f}_P{i}.grib2", f"{f}_P{i}.grib2")
                                os.replace(f"{f}_P{i}.grib2", f"GEM GLOBAL/{p}/{f}_P{i}.grib2")
                                error = False
                            except Exception as e:
                                error = True
                                print(f"Temporarily lost connection to server. Waiting 30 seconds and then trying again to reconnect and resume.")
                                time.sleep(30)
                                retry = retry + 1                             
    

