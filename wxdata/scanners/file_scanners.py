"""
This file hosts the functions that scan files to make sure existing files are up to date. 

(C) Eric J. Drewitz 2025
"""

import os
import time

from wxdata.scanners.checks import *
from wxdata.scanners.keys import *

# Exception handling for Python >= 3.13 and Python < 3.13

from datetime import datetime, timedelta
    
# Gets local time
local = datetime.now()

def file_scanner(model, cat, url, url_run, step, ens_members=False):

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

    aa, bb = index(model)
    hour = forecast_hour(model)
    
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

    exists = False

    if ens_members == False:
        try:
            fnames = []
            for file in os.listdir(f"{model}/{cat}/{step}"):
                fname = os.path.basename(f"{model}/{cat}/{step}/{file}")
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
                modification_timestamp = os.path.getmtime(f"{model}/{cat}/{step}/{fname}")
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
                            max_fcst_hour = forecast_hour(model)
                            download = file_fhour_checker(model, fname, max_fcst_hour)
                
            else:
                download = True

    else:
        members = ensemble_members(f"{model}")
        try:
            fnames = []
            for file in os.listdir(f"{model}/{cat}/{step}/{members}"):
                fname = os.path.basename(f"{model}/{cat}/{step}/{members}/{file}")
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
                modification_timestamp = os.path.getmtime(f"{model}/{cat}/{step}/{members}/{fname}")
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
                            max_fcst_hour = forecast_hour(model)
                            download = file_fhour_checker(model, fname, max_fcst_hour)
                
            else:
                download = True
        
    return download