"""
This file hosts the functions that scan files to make sure existing files are up to date. 

(C) Eric J. Drewitz 2025
"""

import os
import time

from wxdata.scanners.checks import *
from wxdata.scanners.keys import *
from datetime import datetime, timedelta
    
# Gets local time
local = datetime.now()

def rtma_file_scanner(path, fname, model):
    
    """
    This function scans the RTMA files to make sure they are up to date. 
    
    This function will then return a boolean value if new data needs to be downloaded. 
    
    A boolean value of True means the data needs to be updated and False, the data does not need to be updated. 
    
    Required Arguments:
    
    1) path (String) - The path to the files. 
    
    2) fname (String) - The name of the file with the RTMA data. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    A boolean value of True or False if the data needs to be downloaded or not. 
    """
    
    download = False
        
    aa, bb = rtma_files_index(model)
        
    hr = int(f"{fname[aa]}{fname[bb]}")
    
    try:
        for file in os.listdir(f"{path}"):
            name = os.path.basename(f"{path}/{file}")
            
        name_hr = int(f"{name[aa]}{name[bb]}")
        if name_hr == hr:
            pass
        else:
            download = True
    except Exception as e:
        download = True

    if download == False:
        try:
            mtime = os.path.getmtime(f"{path}/{fname}")
            readable_time = time.ctime(mtime)
            update_day = int(f"{readable_time[8]}{readable_time[9]}")
            update_hour = int(f"{readable_time[11]}{readable_time[12]}")
            
            if update_day != local.day:
                download = True
            elif update_day == local.day and update_hour != local.hour:
                download = True
            else:
                download = False
        except Exception as e:
            download = True
        
    return download
    

def gfs_file_scanner(model, cat, directory, url, url_run, step, final_forecast_hour, ens_members=False, members=None):

    """
    This function scans the directory to make sure: 
    
    1) The directory branch exists. 
    2) Builds the directory branch if it does not exist
    3) Makes sure the files are up to date

    Required Arguments: 

    1) model (String) - The model the user wants. 

    2) cat (String) - The category of data the user wants (i.e. ensmean vs. enscontrol). 

    3) url (String) - The URL returned from the url_scanner function. 

    4) url_run (Integer) - The model run time in the URL returned from the url_scanner function. 

    Returns
    -------

    1) A boolean value of True or False for download.
    """    
    model = model.upper()
    cat = cat.upper()
    directory = directory.upper()

    aa, bb = index(model, directory)
    
    if os.path.exists(f"{model}"):
        pass
    else:
        os.mkdir(f"{model}")

    if os.path.exists(f"{model}/{cat}"):
        pass
    else:
        os.mkdir(f"{model}/{cat}")

    if os.path.exists(f"{model}/{cat}/{step}"):
        pass
    else:
        os.mkdir(f"{model}/{cat}/{step}")
        
    if os.path.exists(f"{model}/{cat}/{step}/{directory}"):
        pass
    else:
        os.mkdir(f"{model}/{cat}/{step}/{directory}")      

    exists = False

    if ens_members == False:
        try:
            fnames = []
            for file in os.listdir(f"{model}/{cat}/{step}/{directory}"):
                fname = os.path.basename(f"{model}/{cat}/{step}/{directory}/{file}")
                fnames.append(fname)
            fname = fnames[-1]
            ftype = file_extension(fname)
            exists = True
        except Exception as e:
            download = True
        if exists == False:
            download = True
        else:
            file_run = int(f"{fname[aa]}{fname[bb]}")
            if file_run == url_run:
                modification_timestamp = os.path.getmtime(f"{model}/{cat}/{step}/{directory}/{fname}")
                readable_time = time.ctime(modification_timestamp)
                update_day = int(f"{readable_time[8]}{readable_time[9]}")
                update_hour = int(f"{readable_time[11]}{readable_time[12]}") 
                if update_day != local.day:
                    download = True
                else:
                    tdiff = local - timedelta(hours=6)
                    if update_hour < tdiff.hour:
                        download = True
                    else:
                        if ftype == False:
                            download = True
                        else:
                            download = file_fhour_checker(model, fname, final_forecast_hour)
                
            else:
                download = True

    else:
        members = members[-1]
        try:
            fnames = []
            for file in os.listdir(f"{model}/{cat}/{step}/{directory}/{members}"):
                fname = os.path.basename(f"{model}/{cat}/{step}/{directory}/{members}/{file}")
                fnames.append(fname)
            fname = fnames[-1]
            ftype = file_extension(fname)
            exists = True
        except Exception as e:
            download = True

        if exists == False:
            download = True
    
        else:
            file_run = int(f"{fname[aa]}{fname[bb]}")
            if file_run == url_run:
                modification_timestamp = os.path.getmtime(f"{model}/{cat}/{step}/{directory}/{members}/{fname}")
                readable_time = time.ctime(modification_timestamp)
                update_day = int(f"{readable_time[8]}{readable_time[9]}")
                update_hour = int(f"{readable_time[11]}{readable_time[12]}") 
                if update_day != local.day:
                    download = True
                else:
                    tdiff = local - timedelta(hours=6)
                    if update_hour < tdiff.hour:
                        download = True
                    else:
                        if ftype == False:
                            download = True
                        else:
                            download = file_fhour_checker(model, fname, final_forecast_hour)
                
            else:
                download = True
                    
        
    return download