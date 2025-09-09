"""
This file hosts functions that download various types of GFS and GEFS Data

(C) Eric J. Drewitz 2025
"""


import xarray as xr
import numpy as np
import urllib.request
import os
import sys
import logging
import glob
import warnings
warnings.filterwarnings('ignore')

from wxdata.scanners.url_scanners import gfs_url_scanner
from wxdata.scanners.file_scanners import file_scanner

from wxdata.utils.file_funcs import(
    
    ens_folders, 
    clear_idx_files    
)

from wxdata.utils.coords import shift_longitude
from wxdata.gfs.process import process_data

from wxdata.utils.recycle_bin import *
clear_recycle_bin_windows()
clear_trash_bin_mac()
clear_trash_bin_linux()

try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta

try:
    utc_time = datetime.now(UTC)
except Exception as e:
    utc_time = datetime.utcnow()

local_time = datetime.now()

yesterday = utc_time - timedelta(hours=24)

def gefs_0p50(cat, step=3, western_bound=-180, eastern_bound=180, northern_bound=90, southern_bound=-90, proxies=None, directory='atmos', members='all', final_forecast_hour=384):

    """
    This function retrives the latest GEFS0p50 data. If the data is not previously downloaded nor up to date, the function
    will download and pre-process the latest dataset. 

    To avoid bans from the data servers, the function will scan the data server and locally hosted files and if the 
    files are up to date, the function will skip downloading the newest dataset. 

    Required Arguments:

    1) cat (String) - The category of the data. (i.e. mean, control, all members)

    2) typeOfLevel (String) - This determines which parameters are available for the GEFS 0.25x0.25 Ensemble Mean. The choices are as
       follows: 

      1) surface
      2) meanSea
      3) depthBelowLandLayer
      4) heightAboveGround
      5) atmosphereSingleLayer
      6) cloudCeiling
      7) heightAboveGroundLayer
      8) pressureFromGroundLayer

    Optional Arguments:
    
    1) u_and_v_wind (Boolean) - Default = False. When set to True, the function will return 2 datasets. 
       The first dataset being the u-component of the wind and second dataset the v-component of the wind. 
       When set to False, only 1 dataset is returned. 

    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    6) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }

    7) directory (String) - Default='atmos'. The directory the user wants to download data from.
       Directories: 1) atmos
                    2) chem

    Returns
    -------

    An xarray.data array of the latest GEFS0p25 data for the bounds specified. 
    Files downloaded and pre-processed.                          
    """  
    sys.tracebacklimit = 0
    logging.disable()
    cat = cat.upper()
    model = 'GEFS0P50'
    if final_forecast_hour > 384:
        final_forecast_hour = 384
    
    if step == 6:
        if final_forecast_hour > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = final_forecast_hour + step
    elif step == 3:
        if final_forecast_hour > 100:
            step = 3
            stop = 99 + step
            start = 102
        else:
            step = 3
            stop = final_forecast_hour + step
    else:
        print("ERROR! User entered an invalid step value\nSteps must either be 3 or 6 hourly.")
        sys.exit(1)

    if cat == 'MEAN' or cat == 'CONTROL':
        clear_idx_files(directory=directory, step=step, model=model, cat=cat)
        url, run = gfs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour)
        download = file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour)
        directory = directory.upper()
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        else:
            run = run
            
        if cat == 'MEAN':
            ff = 'avg'
        if cat == 'CONTROL':
            ff = 'c00'
        if download == True:
            print(f"Downloading the latest {model} data...")
    
            for file in os.listdir(f"{model}/{cat}/{step}/{directory}"):
                try:
                    os.remove(f"{model}/{cat}/{step}/{directory}/{file}")
                except Exception as e:
                    pass
                
            if directory == 'ATMOS':
            
                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2a.0p50.f00{i}", f"ge{ff}.t{run}z.pgrb2a.0p50.f00{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2a.0p50.f00{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50.f00{i}")
                    else:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2a.0p50.f0{i}", f"ge{ff}.t{run}z.pgrb2a.0p50.f0{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2a.0p50.f0{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50.f0{i}")
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2a.0p50.f{i}", f"ge{ff}.t{run}z.pgrb2a.0p50.f{i}")
                            os.replace(f"ge{ff}.t{run}z.pgrb2a.0p50.f{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50.f{i}") 
                        except Exception as e:
                            pass 

                for i in range(0, stop, step):
                    if i < 10:
                        try:
                            os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50.f00{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50_f00{i}.grib2")
                        except Exception as e:
                            pass
                    else:
                        try:
                            os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50.f0{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50_f0{i}.grib2")
                        except Exception as e:
                            pass
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50.f{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50_f{i}.grib2")
                        except Exception as e:
                            pass    
                        
            else:
                
                if final_forecast_hour >= 120:
                    final_forecast_hour = 120
                    
                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}gefs.chem.t{run}z.a3d_0p50.f00{i}.grib2", f"gefs.chem.t{run}z.a3d_0p50.f00{i}.grib2")
                        os.replace(f"gefs.chem.t{run}z.a3d_0p50.f00{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.chem.t{run}z.a3d_0p50.f00{i}.grib2")
                    else:
                        urllib.request.urlretrieve(f"{url}gefs.chem.t{run}z.a3d_0p50.f0{i}.grib2", f"gefs.chem.t{run}z.a3d_0p50.f0{i}.grib2")
                        os.replace(f"gefs.chem.t{run}z.a3d_0p50.f0{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.chem.t{run}z.a3d_0p50.f0{i}.grib2")
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}gefs.chem.t{run}z.a3d_0p50.f{i}.grib2", f"gefs.chem.t{run}z.a3d_0p50.f{i}.grib2")
                            os.replace(f"gefs.chem.t{run}z.a3d_0p50.f{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.chem.t{run}z.a3d_0p50.f{i}.grib2") 
                        except Exception as e:
                            pass              

        else:
            print(f"Data in f:{model}/{cat}/{step} is current. Skipping download.")
        
        ds = process_data(model, cat, step, directory, western_bound, eastern_bound, northern_bound, southern_bound, False)

        clear_idx_files(directory=directory, step=step, model=model, cat=cat)

    else:
        
        try:
            members = members.lower()
        except Exception as e:
            pass
        
        try:
            if members == 'all':
                members = np.arange(0, 31, 1)
            else:
                members = members
        except Exception as e:
            members = members
            
        paths = ens_folders(model, cat, step, directory, members)
        clear_idx_files(paths=paths, ens=True)
        url, run = gfs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour, members=members)
        download = file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour, ens_members=True, members=members)
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        else:
            run = run

        if download == True:
            print(f"Downloading the latest {model} data...")
            for pp in paths:
                for file in os.listdir(f"{pp}"):
                    try:
                        os.remove(f"{pp}/{file}")
                    except Exception as e:
                        pass            

            for e, p in zip(members, paths):
                if e < 10:
                    ff = f"p0{e}"
                else:
                    ff = f"p{e}"
                        
                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2a.0p50.f00{i}", f"ge{ff}.t{run}z.pgrb2a.0p50.f00{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2a.0p50.f00{i}", f"{p}/ge{ff}.t{run}z.pgrb2a.0p50.f00{i}")
                    else:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2a.0p50.f0{i}", f"ge{ff}.t{run}z.pgrb2a.0p50.f0{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2a.0p50.f0{i}", f"{p}/ge{ff}.t{run}z.pgrb2a.0p50.f0{i}")
                        
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2a.0p50.f{i}", f"ge{ff}.t{run}z.pgrb2a.0p50.f{i}")
                            os.replace(f"ge{ff}.t{run}z.pgrb2a.0p50.f{i}", f"{p}/ge{ff}.t{run}z.pgrb2a.0p50.f{i}")  
                        except Exception as e:
                            pass
                            
                for i in range(0, stop, step):
                    if i < 10:
                        try:
                            os.replace(f"{p}/ge{ff}.t{run}z.pgrb2a.0p50.f00{i}", f"{p}/ge{ff}.t{run}z.pgrb2a.0p50_f00{i}.grib2")
                        except Exception as e:
                            pass
                    else:
                        try:
                            os.replace(f"{p}/ge{ff}.t{run}z.pgrb2a.0p50.f0{i}", f"{p}/ge{ff}.t{run}z.pgrb2a.0p50_f0{i}.grib2")
                        except Exception as e:
                            pass
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            os.replace(f"{p}/ge{ff}.t{run}z.pgrb2a.0p50.f{i}", f"{p}/ge{ff}.t{run}z.pgrb2a.0p50_f{i}.grib2")
                        except Exception as e:
                            pass    

        else:
            print(f"Data in f:{model}/{cat} is current. Skipping download.")

        ds = process_data(model, cat, step, directory, western_bound, eastern_bound, northern_bound, southern_bound, True)
        clear_idx_files(paths=paths, ens=True)
        
    return ds


def gefs_0p50_secondary_parameters(cat, step=3, western_bound=-180, eastern_bound=180, northern_bound=90, southern_bound=-90, proxies=None, members='all', final_forecast_hour=384):

    """
    This function retrives the latest GEFS0p50 data. If the data is not previously downloaded nor up to date, the function
    will download and pre-process the latest dataset. 

    To avoid bans from the data servers, the function will scan the data server and locally hosted files and if the 
    files are up to date, the function will skip downloading the newest dataset. 

    Required Arguments:

    1) cat (String) - The category of the data. (i.e. mean, control, all members)

    2) typeOfLevel (String) - This determines which parameters are available for the GEFS 0.25x0.25 Ensemble Mean. The choices are as
       follows: 

      1) surface
      2) meanSea
      3) depthBelowLandLayer
      4) heightAboveGround
      5) atmosphereSingleLayer
      6) cloudCeiling
      7) heightAboveGroundLayer
      8) pressureFromGroundLayer

    Optional Arguments:
    
    1) u_and_v_wind (Boolean) - Default = False. When set to True, the function will return 2 datasets. 
       The first dataset being the u-component of the wind and second dataset the v-component of the wind. 
       When set to False, only 1 dataset is returned. 

    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    6) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
                        
    7) directory (String) - Default='atmos'. The directory the user wants to download data from.
       Directories: 1) atmos

    Returns
    -------

    An xarray.data array of the latest GEFS0p25 data for the bounds specified. 
    Files downloaded and pre-processed.                          
    """  
    sys.tracebacklimit = 0
    logging.disable()
    cat = cat.upper()
    model = 'GEFS0P50 SECONDARY PARAMETERS'
    directory = 'atmos'
    if final_forecast_hour > 384:
        final_forecast_hour = 384
    
    if cat == 'MEAN':
        cat = 'CONTROL'
    
    if step == 6:
        if final_forecast_hour > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = final_forecast_hour + step
    elif step == 3:
        if final_forecast_hour > 100:
            step = 3
            stop = 99 + step
            start = 102
        else:
            step = 3
            stop = final_forecast_hour + step
    else:
        print("ERROR! User entered an invalid step value\nSteps must either be 3 or 6 hourly.")
        sys.exit(1)

    if cat == 'CONTROL':
        clear_idx_files(directory=directory, step=step, model=model, cat=cat)
        url, run = gfs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour)
        download = file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour)
        directory = directory.upper()
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        else:
            run = run
            
        if cat == 'CONTROL':
            ff = 'c00'
        if download == True:
            print(f"Downloading the latest {model} data...")
    
            for file in os.listdir(f"{model}/{cat}/{step}/{directory}"):
                try:
                    os.remove(f"{model}/{cat}/{step}/{directory}/{file}")
                except Exception as e:
                    pass
            
            for i in range(0, stop, step):
                if i < 10:
                    urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2b.0p50.f00{i}", f"ge{ff}.t{run}z.pgrb2b.0p50.f00{i}")
                    os.replace(f"ge{ff}.t{run}z.pgrb2b.0p50.f00{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50.f00{i}")
                else:
                    urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2b.0p50.f0{i}", f"ge{ff}.t{run}z.pgrb2b.0p50.f0{i}")
                    os.replace(f"ge{ff}.t{run}z.pgrb2b.0p50.f0{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50.f0{i}")
            if final_forecast_hour > 100:
                for i in range(start, final_forecast_hour + step, step):
                    try:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2b.0p50.f{i}", f"ge{ff}.t{run}z.pgrb2b.0p50.f{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2b.0p50.f{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50.f{i}") 
                    except Exception as e:
                        pass 

            for i in range(0, stop, step):
                if i < 10:
                    try:
                        os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50.f00{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50_f00{i}.grib2")
                    except Exception as e:
                        pass
                else:
                    try:
                        os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50.f0{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50_f0{i}.grib2")
                    except Exception as e:
                        pass
            if final_forecast_hour > 100:
                for i in range(start, final_forecast_hour + step, step):
                    try:
                        os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50.f{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50_f{i}.grib2")
                    except Exception as e:
                        pass    
                        

        else:
            print(f"Data in f:{model}/{cat}/{step} is current. Skipping download.")
        
        ds = process_data(model, cat, step, directory, western_bound, eastern_bound, northern_bound, southern_bound, False)

        clear_idx_files(directory=directory, step=step, model=model, cat=cat)

    else:
        
        try:
            members = members.lower()
        except Exception as e:
            pass
        
        try:
            if members == 'all':
                members = np.arange(0, 31, 1)
            else:
                members = members
        except Exception as e:
            members = members
            
        paths = ens_folders(model, cat, step, directory, members)
        clear_idx_files(paths=paths, ens=True)
        url, run = gfs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour, members=members)
        download = file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour, ens_members=True, members=members)
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        else:
            run = run

        if download == True:
            print(f"Downloading the latest {model} data...")
            for pp in paths:
                for file in os.listdir(f"{pp}"):
                    try:
                        os.remove(f"{pp}/{file}")
                    except Exception as e:
                        pass            

            for e, p in zip(members, paths):
                if e < 10:
                    ff = f"p0{e}"
                else:
                    ff = f"p{e}"
                        
                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2b.0p50.f00{i}", f"ge{ff}.t{run}z.pgrb2b.0p50.f00{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2b.0p50.f00{i}", f"{p}/ge{ff}.t{run}z.pgrb2b.0p50.f00{i}")
                    else:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2b.0p50.f0{i}", f"ge{ff}.t{run}z.pgrb2b.0p50.f0{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2b.0p50.f0{i}", f"{p}/ge{ff}.t{run}z.pgrb2b.0p50.f0{i}")
                        
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2b.0p50.f{i}", f"ge{ff}.t{run}z.pgrb2b.0p50.f{i}")
                            os.replace(f"ge{ff}.t{run}z.pgrb2b.0p50.f{i}", f"{p}/ge{ff}.t{run}z.pgrb2b.0p50.f{i}")  
                        except Exception as e:
                            pass
                            
                for i in range(0, stop, step):
                    if i < 10:
                        try:
                            os.replace(f"{p}/ge{ff}.t{run}z.pgrb2b.0p50.f00{i}", f"{p}/ge{ff}.t{run}z.pgrb2b.0p50_f00{i}.grib2")
                        except Exception as e:
                            pass
                    else:
                        try:
                            os.replace(f"{p}/ge{ff}.t{run}z.pgrb2b.0p50.f0{i}", f"{p}/ge{ff}.t{run}z.pgrb2b.0p50_f0{i}.grib2")
                        except Exception as e:
                            pass
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            os.replace(f"{p}/ge{ff}.t{run}z.pgrb2b.0p50.f{i}", f"{p}/ge{ff}.t{run}z.pgrb2b.0p50_f{i}.grib2")
                        except Exception as e:
                            pass    

        else:
            print(f"Data in f:{model}/{cat} is current. Skipping download.")

        ds = process_data(model, cat, step, directory, western_bound, eastern_bound, northern_bound, southern_bound, True)
        clear_idx_files(paths=paths, ens=True)
        
    return ds



def gefs_0p25(cat, step=3, u_and_v_wind=False, western_bound=-180, eastern_bound=180, northern_bound=90, southern_bound=-90, proxies=None, directory='atmos', members='all', final_forecast_hour=384):

    """
    This function retrives the latest GEFS0p25 data. If the data is not previously downloaded nor up to date, the function
    will download and pre-process the latest dataset. 

    To avoid bans from the data servers, the function will scan the data server and locally hosted files and if the 
    files are up to date, the function will skip downloading the newest dataset. 

    Required Arguments:

    1) cat (String) - The category of the data. (i.e. mean, control, all members)

    2) typeOfLevel (String) - This determines which parameters are available for the GEFS 0.25x0.25 Ensemble Mean. The choices are as
       follows: 

      1) surface
      2) meanSea
      3) depthBelowLandLayer
      4) heightAboveGround
      5) atmosphereSingleLayer
      6) cloudCeiling
      7) heightAboveGroundLayer
      8) pressureFromGroundLayer

    Optional Arguments:
    
    1) u_and_v_wind (Boolean) - Default = False. When set to True, the function will return 2 datasets. 
       The first dataset being the u-component of the wind and second dataset the v-component of the wind. 
       When set to False, only 1 dataset is returned. 

    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    6) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }

    7) directory (String) - Default='atmos'. The directory the user wants to download data from.
       Directories: 1) atmos
                    2) chem
                    3) wave
    Returns
    -------

    An xarray.data array of the latest GEFS0p25 data for the bounds specified. 
    Files downloaded and pre-processed.                          
    """  
    sys.tracebacklimit = 0
    logging.disable()
    cat = cat.upper()
    model = 'GEFS0P25'
    directory = directory.lower()
    
    if final_forecast_hour > 240 and directory != 'wave':
        final_forecast_hour = 240
    else:
        final_forecast_hour = final_forecast_hour
        if final_forecast_hour > 384:
            final_forecast_hour = 384
        else:
            final_forecast_hour = final_forecast_hour
    
    if step == 6:
        if final_forecast_hour > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = final_forecast_hour + step
    elif step == 3:
        if final_forecast_hour > 100:
            step = 3
            stop = 99 + step
            start = 102
        else:
            step = 3
            stop = final_forecast_hour + step
    else:
        print("ERROR! User entered an invalid step value\nSteps must either be 3 or 6 hourly.")
        sys.exit(1)

    if cat == 'MEAN' or cat == 'CONTROL' or cat == 'SPREAD' or cat == 'PROB':
        clear_idx_files(directory=directory, step=step, model=model, cat=cat)
        url, run = gfs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour)
        download = file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour)
        directory = directory.upper()
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        else:
            run = run
            
        if cat == 'MEAN':
            ff = 'avg'
        if cat == 'CONTROL':
            ff = 'c00'
        if download == True:
            print(f"Downloading the latest {model} data...")
    
            for file in os.listdir(f"{model}/{cat}/{step}/{directory}"):
                try:
                    os.remove(f"{model}/{cat}/{step}/{directory}/{file}")
                except Exception as e:
                    pass
                
            if directory == 'ATMOS':
                
                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f00{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}")
                    else:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f0{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}")
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f{i}")
                            os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}") 
                        except Exception as e:
                            pass 

                for i in range(0, stop, step):
                    if i < 10:
                        try:
                            os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25_f00{i}.grib2")
                        except Exception as e:
                            pass
                    else:
                        try:
                            os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25_f0{i}.grib2")
                        except Exception as e:
                            pass
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25_f{i}.grib2")
                        except Exception as e:
                            pass    
                        
            elif directory == 'CHEM':
                
                if final_forecast_hour >= 120:
                    final_forecast_hour = 120
                    
                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}gefs.chem.t{run}z.a2d_0p25.f00{i}.grib2", f"gefs.chem.t{run}z.a2d_0p25.f00{i}.grib2")
                        os.replace(f"gefs.chem.t{run}z.a2d_0p25.f00{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.chem.t{run}z.a2d_0p25.f00{i}.grib2")
                    else:
                        urllib.request.urlretrieve(f"{url}gefs.chem.t{run}z.a2d_0p25.f0{i}.grib2", f"gefs.chem.t{run}z.a2d_0p25.f0{i}.grib2")
                        os.replace(f"gefs.chem.t{run}z.a2d_0p25.f0{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.chem.t{run}z.a2d_0p25.f0{i}.grib2")
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}gefs.chem.t{run}z.a2d_0p25.f{i}.grib2", f"gefs.chem.t{run}z.a2d_0p25.f{i}.grib2")
                            os.replace(f"gefs.chem.t{run}z.a2d_0p25.f{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.chem.t{run}z.a2d_0p25.f{i}.grib2") 
                        except Exception as e:
                            pass 
                        
            else:
                cat = cat.lower()
                if cat == 'control':
                    ct = 'c00'
                else:
                    ct = cat.lower()

                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}gefs.wave.t{run}z.{ct}.global.0p25.f00{i}.grib2", f"gefs.wave.t{run}z.{ct}.global.0p25.f00{i}.grib2")
                        os.replace(f"gefs.wave.t{run}z.{ct}.global.0p25.f00{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.wave.t{run}z.{cat}.global.0p25.f00{i}.grib2")
                    else:
                        urllib.request.urlretrieve(f"{url}gefs.wave.t{run}z.{ct}.global.0p25.f0{i}.grib2", f"gefs.wave.t{run}z.{ct}.global.0p25.f0{i}.grib2")
                        os.replace(f"gefs.wave.t{run}z.{ct}.global.0p25.f0{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.wave.t{run}z.{cat}.global.0p25.f0{i}.grib2")
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}gefs.wave.t{run}z.{ct}.global.0p25.f{i}.grib2", f"gefs.wave.t{run}z.{ct}.global.0p25.f{i}.grib2")
                            os.replace(f"gefs.wave.t{run}z.{ct}.global.0p25.f{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.wave.t{run}z.{cat}.global.0p25.f{i}.grib2") 
                        except Exception as e:
                            pass 
                  

            

        else:
            print(f"Data in f:{model}/{cat}/{step} is current. Skipping download.")
        
        ds = process_data(model, cat, step, directory, western_bound, eastern_bound, northern_bound, southern_bound, False)

        clear_idx_files(directory=directory, step=step, model=model, cat=cat)

    else:
        
        try:
            members = members.lower()
        except Exception as e:
            pass
        
        try:
            if members == 'all':
                members = np.arange(0, 31, 1)
            else:
                members = members
        except Exception as e:
            members = members
            
        paths = ens_folders(model, cat, step, directory, members)
        clear_idx_files(paths=paths, ens=True)
        url, run = gfs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour, members=members)
        download = file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour, ens_members=True, members=members)
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        else:
            run = run

        if download == True:
            print(f"Downloading the latest {model} data...")
            for pp in paths:
                for file in os.listdir(f"{pp}"):
                    try:
                        os.remove(f"{pp}/{file}")
                    except Exception as e:
                        pass            

            for e, p in zip(members, paths):
                if e < 10:
                    ff = f"p0{e}"
                else:
                    ff = f"p{e}"
                        
                if directory == 'ATMOS':
                    for i in range(0, stop, step):
                        if i < 10:
                            urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f00{i}")
                            os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"{p}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}")
                        else:
                            urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f0{i}")
                            os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"{p}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}")
                            
                    if final_forecast_hour > 100:
                        for i in range(start, final_forecast_hour + step, step):
                            try:
                                urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f{i}")
                                os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"{p}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}")  
                            except Exception as e:
                                pass
                                
                    for i in range(0, stop, step):
                        if i < 10:
                            try:
                                os.replace(f"{p}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"{p}/ge{ff}.t{run}z.pgrb2s.0p25_f00{i}.grib2")
                            except Exception as e:
                                pass
                        else:
                            try:
                                os.replace(f"{p}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"{p}/ge{ff}.t{run}z.pgrb2s.0p25_f0{i}.grib2")
                            except Exception as e:
                                pass
                    if final_forecast_hour > 100:
                        for i in range(start, final_forecast_hour + step, step):
                            try:
                                os.replace(f"{p}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"{p}/ge{ff}.t{run}z.pgrb2s.0p25_f{i}.grib2")
                            except Exception as e:
                                pass    
                            
                else:
                    
                    for i in range(0, stop, step):
                        if i < 10:
                            urllib.request.urlretrieve(f"{url}gefs.wave.t{run}z.{ff}.global.0p25.f00{i}.grib2", f"gefs.wave.t{run}z.{ff}.global.0p25.f00{i}.grib2")
                            os.replace(f"gefs.wave.t{run}z.{ff}.global.0p25.f00{i}.grib2", f"{p}/gefs.wave.t{run}z.{ff}.global.0p25.f00{i}.grib2")
                        else:
                            urllib.request.urlretrieve(f"{url}gefs.wave.t{run}z.{ff}.global.0p25.f0{i}.grib2", f"gefs.wave.t{run}z.{ff}.global.0p25.f0{i}.grib2")
                            os.replace(f"gefs.wave.t{run}z.{ff}.global.0p25.f0{i}.grib2", f"{p}/gefs.wave.t{run}z.{ff}.global.0p25.f0{i}.grib2")
                            
                    if final_forecast_hour > 100:
                        for i in range(start, final_forecast_hour + step, step):
                            try:
                                urllib.request.urlretrieve(f"{url}gefs.wave.t{run}z.{ff}.global.0p25.f{i}.grib2", f"gefs.wave.t{run}z.{ff}.global.0p25.f{i}.grib2")
                                os.replace(f"gefs.wave.t{run}z.{ff}.global.0p25.f{i}.grib2", f"{p}/gefs.wave.t{run}z.{ff}.global.0p25.f{i}.grib2")  
                            except Exception as e:
                                pass
                                

        else:
            print(f"Data in f:{model}/{cat} is current. Skipping download.")

        ds = process_data(model, cat, step, directory, western_bound, eastern_bound, northern_bound, southern_bound, True)
        clear_idx_files(paths=paths, ens=True)
        
    return ds

            
