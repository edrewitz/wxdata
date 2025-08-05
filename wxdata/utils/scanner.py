"""
This file has the scanner function which scans the data server for the latest FULL dataset and returns the download url

(C) Eric J. Drewitz 
"""

# Imports the needed packages
import requests
import os
import time

# Exception handling for Python >= 3.13 and Python < 3.13
try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta

# Gets current time in UTC
try:
    now = datetime.now(UTC)
except Exception as e:
    now = datetime.utcnow()

# Gets local time
local = datetime.now()

# Gets yesterday's date
yd = now - timedelta(days=1)

def file_extension(fname):

    """
    Scans for file extension.
    """

    if fname[-4] == 'f':
        ftype = False
    else:
        ftype = True

    return ftype

def file_fhour_checker(model, fname, max_fcst_hour):

    """
    This function returns the string-index of the model run times in a file

    1) model (String) - The forecast model

    Optional Arguments: None

    Returns
    -------

    The index values of the run times in the file. 
    """
    
    hr = int(f"{fname[-9]}{fname[-8]}{fname[-7]}")

    if hr == max_fcst_hour:
        download = False
    else:
        download = True

    return download


def forecast_hour(model):

    """
    This function returns the latest forecast hour for each model
    """

    hour = {
        'GEFS0P25':240,
        'GEFS0P50':384,
        'GEFS0P50 SECONDARY PARAMETERS':384,
        'GFS0P25':384,
        'GFS0P25 SECONDARY PARAMETERS':384        
    }
    
    return hour[model]

def ensemble_members(model):

    """
    This function returns the number of ensemble members for an ensemble

    Required Arguments:

    1) model (String)

    Returns
    -------
    The number of ensemble members for a particular ensemble
    """

    members = {
        'GEFS0P25':30,
        'GEFS0P50':30,
        'GEFS0P50 SECONDARY PARAMETERS':30
        
    }

    return members[model]
        
def url_index(model):

    """
    This function returns the string-index of the model run times in a file

    1) model (String) - The forecast model

    Optional Arguments: None

    Returns
    -------

    The index values of the run times in the file. 
    """
    
    times = {
        'GEFS0P25':[-19, -18],
        'GEFS0P50':[-18, -17],
        'GEFS0P50 SECONDARY PARAMETERS':[-18, -17],
        'GFS0P25':[-9, -8],
        'GFS0P25 SECONDARY PARAMETERS':[-9, -8]
    }

    return times[model][0], times[model][1]


def index(model):

    """
    This function returns the string-index of the model run times in a file

    1) model (String) - The forecast model

    Optional Arguments: None

    Returns
    -------

    The index values of the run times in the file. 
    """
    
    times = {
        'GEFS0P25':[7, 8],
        'GEFS0P50':[7, 8],
        'GEFS0P50 SECONDARY PARAMETERS':[7, 8],
        'GFS0P25':[5, 6],
        'GFS0P25 SECONDARY PARAMETERS':[5, 6]
    }

    return times[model][0], times[model][1]

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
    

def url_scanner(model, cat, proxies, directory):

    """
    This function scans a webpage for the file with the latest forecast model run. 
    If the page has complete data, the download link will be returned. 
    If the page is incomplete, the scanner will check for the previous run data. 
    This scanner is used so the user downloads the latest FULL dataset. 

    Required Arguments: 

    1) model (String) - The model the user wants. 

    2) cat (String) - The category of data the user wants (i.e. ensmean vs. enscontrol). 

    3) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                        }
                        
    4) directory (String) - The directory the user wants to scan.
       Directories: 1) atmos
                    2) chem
                    3) wave
    
    Optional Arguments: None

    Returns
    -------

    1) The download link.
    2) The time of the latest model run. 
    """
    model = model.upper()
    cat = cat.upper()
    directory = directory.lower()

    aa, bb = url_index(model)
    
    print(aa, bb)
    
    if model == 'GFS0P25' or model == 'GFS0P25 SECONDARY PARAMETERS':
        today_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/00/{directory}/"
        today_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/06/{directory}/"
        today_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/12/{directory}/"
        today_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/18/{directory}/"
        
        yday_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/00/{directory}/"
        yday_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/06/{directory}/"
        yday_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/12/{directory}/"
        yday_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/18/{directory}/"
        
        if model == 'GFS0P25':
            f_00z = "gfs.t00z.pgrb2.0p25.f384"
            f_06z = "gfs.t06z.pgrb2.0p25.f384"
            f_12z = "gfs.t12z.pgrb2.0p25.f384"
            f_18z = "gfs.t18z.pgrb2.0p25.f384"
        else:
            f_00z = "gfs.t00z.pgrb2b.0p25.f384"
            f_06z = "gfs.t06z.pgrb2b.0p25.f384"
            f_12z = "gfs.t12z.pgrb2b.0p25.f384"
            f_18z = "gfs.t18z.pgrb2b.0p25.f384"
    
    if model == 'GEFS0P25' or model == 'GEFS0P50' or model == 'GEFS0P50 SECONDARY PARAMETERS':
        if model == 'GEFS0P25':
            a = 's'
            b = '25'
            c = '25'
            
        if model == 'GEFS0P50':
            a = 'a'
            b = '5'
            c = '50'

        if model == 'GEFS0P50 SECONDARY PARAMETERS':
            a = 'b'
            b = '5'
            c = '50'

        today_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/00/{directory}/pgrb2{a}p{b}/"
        today_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/06/{directory}/pgrb2{a}p{b}/"
        today_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/12/{directory}/pgrb2{a}p{b}/"
        today_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/18/{directory}/pgrb2{a}p{b}/"
        
        yday_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/00/{directory}/pgrb2{a}p{b}/"
        yday_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/06/{directory}/pgrb2{a}p{b}/"
        yday_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/12/{directory}/pgrb2{a}p{b}/"
        yday_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/18/{directory}/pgrb2{a}p{b}/"
    
        if cat == 'MEAN':
            if model == 'GEFS0P50 SECONDARY PARAMETERS':
                f_00z = f"gec00.t00z.pgrb2{a}.0p{c}.f240"
                f_06z = f"gec00.t06z.pgrb2{a}.0p{c}.f240"
                f_12z = f"gec00.t12z.pgrb2{a}.0p{c}.f240"
                f_18z = f"gec00.t18z.pgrb2{a}.0p{c}.f240"                 
            else:
                f_00z = f"geavg.t00z.pgrb2{a}.0p{c}.f240"
                f_06z = f"geavg.t06z.pgrb2{a}.0p{c}.f240"
                f_12z = f"geavg.t12z.pgrb2{a}.0p{c}.f240"
                f_18z = f"geavg.t18z.pgrb2{a}.0p{c}.f240"
        if cat == 'CONTROL':
            f_00z = f"gec00.t00z.pgrb2{a}.0p{c}.f240"
            f_06z = f"gec00.t06z.pgrb2{a}.0p{c}.f240"
            f_12z = f"gec00.t12z.pgrb2{a}.0p{c}.f240"
            f_18z = f"gec00.t18z.pgrb2{a}.0p{c}.f240"  
        if cat == 'ALL MEMBERS':
            f_00z = f"gep30.t00z.pgrb2{a}.0p{c}.f240"
            f_06z = f"gep30.t06z.pgrb2{a}.0p{c}.f240"
            f_12z = f"gep30.t12z.pgrb2{a}.0p{c}.f240"
            f_18z = f"gep30.t18z.pgrb2{a}.0p{c}.f240"         
    
    if proxies == None:
        t_18z = requests.get(f"{today_18z}/{f_18z}", stream=True)
        t_12z = requests.get(f"{today_12z}/{f_12z}", stream=True)
        t_06z = requests.get(f"{today_06z}/{f_06z}", stream=True)
        t_00z = requests.get(f"{today_00z}/{f_00z}", stream=True)

        y_18z = requests.get(f"{yday_18z}/{f_18z}", stream=True)
        y_12z = requests.get(f"{yday_12z}/{f_12z}", stream=True)
        y_06z = requests.get(f"{yday_06z}/{f_06z}", stream=True)
        y_00z = requests.get(f"{yday_00z}/{f_00z}", stream=True)    

    else:
        t_18z = requests.get(f"{today_18z}/{f_18z}", stream=True, proxies=proxies)
        t_12z = requests.get(f"{today_12z}/{f_12z}", stream=True, proxies=proxies)
        t_06z = requests.get(f"{today_06z}/{f_06z}", stream=True, proxies=proxies)
        t_00z = requests.get(f"{today_00z}/{f_00z}", stream=True, proxies=proxies)

        y_18z = requests.get(f"{yday_18z}/{f_18z}", stream=True, proxies=proxies)
        y_12z = requests.get(f"{yday_12z}/{f_12z}", stream=True, proxies=proxies)
        y_06z = requests.get(f"{yday_06z}/{f_06z}", stream=True, proxies=proxies)
        y_00z = requests.get(f"{yday_00z}/{f_00z}", stream=True, proxies=proxies)         

    if t_18z.status_code == 200:
        url = f"{today_18z}"
    elif t_18z.status_code != 200 and t_12z.status_code == 200:
        url = f"{today_12z}"
    elif t_12z.status_code != 200 and t_06z.status_code == 200:
        url = f"{today_06z}"
    elif t_06z.status_code != 200 and t_00z.status_code == 200:
        url = f"{today_00z}"
    elif t_00z.status_code != 200 and y_18z.status_code == 200:
        url = f"{yday_18z}"
    elif y_18z.status_code != 200 and y_12z.status_code == 200:
        url = f"{yday_12z}"
    elif y_12z.status_code != 200 and y_06z.status_code == 200:
        url = f"{yday_06z}"
    else:
        url = f"{yday_00z}"

    url_run = int(f"{url[aa]}{url[bb]}")
    
    print(url)
    print(url_run)
        
    return url, url_run
