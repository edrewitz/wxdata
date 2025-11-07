
"""
This file hosts the functions that scan files to make sure existing files are up to date. 

(C) Eric J. Drewitz 2025
"""

import os
import time

from datetime import datetime, timedelta
    
# Gets local time
local = datetime.now()

def extract_runtime(filename):
    
    """
    This function extracts the run time from the filename.
    
    Required Arguments:
    
    1) filename (String) - The filename.  
    
    Optional Arguments: None
    
    Returns
    -------
    
    The model run time.     
    """
    
    keys = ['rtma', 
            'blend']
    
    for key in keys:
        if key in filename:
            step = 1
        else:
            step = 6
    
    keywords = []
    for i in range(0, 24, step):
        if i < 10:
            keyword = f"t0{i}z"
        else:
            keyword = f"t{i}z"
            
        keywords.append(keyword)
    
    for keyword in keywords:
        if keyword in filename:
            run = int(f"{keyword[1]}{keyword[2]}")    
        
            
    return run



def local_file_scanner(path, 
                          filename,
                          source,
                          run,
                          model='aifs'):
    
    """
    This function scans the file on the desktop to make sure it is up to date with the latest data.
    
    Required Arguments:
    
    1) path (String) - A the path to the file. 
    
    2) filename (String) - The filename.
    
    3) source (String) - The data source since different files have different filenames.
    
    4) run (Integer) - The model run scanned from the URL Scanner. 
    
    sources
    -------
    
    1) nomads
    2) ecmwf
    
    Optional Arguments: 
    
    1) model (String) - Default='aifs'. **FOR ECMWF ONLY**
       Operational IFS data updates every 12 hours. This is how we will reflect this below
       with determining whether new data needs to be downloaded. 
    
    Returns
    -------
    
    A boolean value whether the data needs updating.
    """
    
    download = False
    
    if source == 'nomads':
        if os.path.exists(f"{path}/{filename}.grib2"):
            modification_timestamp = os.path.getmtime(f"{path}/{filename}.grib2")
            readable_time = time.ctime(modification_timestamp)
            update_day = int(f"{readable_time[8]}{readable_time[9]}")
            update_hour = int(f"{readable_time[11]}{readable_time[12]}") 
            if update_day != local.day:
                download = True
            else:
                latest = os.path.basename(f"{path}/{filename}.grib2")
                mrun = extract_runtime(filename)
                if run == mrun:
                    pass
                else:
                    download = True
                tdiff = local.hour - update_hour
                if tdiff <= 6:
                    pass
                else:
                    download = True
        else:
            download = True
    else:
        if os.path.exists(f"{path}/{filename}"):
            modification_timestamp = os.path.getmtime(f"{path}/{filename}")
            readable_time = time.ctime(modification_timestamp)
            update_day = int(f"{readable_time[8]}{readable_time[9]}")
            update_hour = int(f"{readable_time[11]}{readable_time[12]}") 
            if update_day != local.day:
                download = True
            else:
                latest = os.path.basename(f"{path}/{filename}")
                mrun = int(f"{latest[8]}{latest[9]}")
                if run == mrun:
                    pass
                else:
                    download = True
                
                tdiff = local.hour - update_hour
                if model == 'operational ifs':
                  if tdiff <= 12:
                      pass
                  else:
                      download = True
                    
                else:
                    if tdiff <= 6:
                        pass
                    else:
                        download = True
        else:
            download = True        
        
    return download