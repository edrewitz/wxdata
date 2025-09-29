
"""
This file hosts the functions that scan files to make sure existing files are up to date. 

(C) Eric J. Drewitz 2025
"""

import os
import time

from datetime import datetime, timedelta
    
# Gets local time
local = datetime.now()

def local_file_scanner(path, 
                          filename):
    
    """
    This function scans the file on the desktop to make sure it is up to date with the latest data.
    
    Required Arguments:
    
    1) path (String) - A the path to the file. 
    
    2) filename (String) - The filename.
    
    Optional Arguments: None
    
    Returns
    -------
    
    A boolean value whether the data needs updating.
    """
    
    download = False
    if os.path.exists(f"{path}/{filename}.grib2"):
        modification_timestamp = os.path.getmtime(f"{path}/{filename}.grib2")
        readable_time = time.ctime(modification_timestamp)
        update_day = int(f"{readable_time[8]}{readable_time[9]}")
        update_hour = int(f"{readable_time[11]}{readable_time[12]}") 
        if update_day != local.day:
            download = True
        else:
            tdiff = local.hour - update_hour
            if tdiff <= 6:
                pass
            else:
                download = True
    else:
        download = True
        
    return download