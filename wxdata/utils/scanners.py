"""
This file has the scanner function which scans the data server for the latest FULL dataset and returns the download url

(C) Eric J. Drewitz 2025
"""

# Imports the needed packages
import requests
import os
import sys
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
        
def url_index(model, directory):

    """
    This function returns the string-index of the model run times in a file

    1) model (String) - The forecast model

    2) directory (String) - The directory the user wants to scan

    Optional Arguments: None

    Returns
    -------

    The index values of the run times in the file. 
    """
    
    if directory == 'atmos':
    
        times = {
            'GEFS0P25':[-19, -18],
            'GEFS0P50':[-18, -17],
            'GEFS0P50 SECONDARY PARAMETERS':[-18, -17],
            'GFS0P25':[-9, -8],
            'GFS0P25 SECONDARY PARAMETERS':[-9, -8]
        }
        
    elif directory == 'chem':

        times = {
            'GEFS0P25':[-18, -17],
            'GEFS0P50':[-18, -17],
            'GEFS0P50 SECONDARY PARAMETERS':[-18, -17],
            'GFS0P25':[-9, -8],
            'GFS0P25 SECONDARY PARAMETERS':[-9, -8]
        }
        
    else:
        
        times = {
            'GEFS0P25':[-16, -15],
            'GEFS0P50':[-16, -15],
            'GEFS0P50 SECONDARY PARAMETERS':[-16, -15],
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
    

def gfs_url_scanner(model, cat, proxies, directory):

    """
    This function scans a webpage for the file with the latest GFS/GEFS forecast model run. 
    If the page has complete data, the download link will be returned. 
    If the page is incomplete, the scanner will check for the previous run data. 
    This scanner is used so the user downloads the latest FULL dataset. 

    Required Arguments: 

    1) model (String) - The model the user wants. 
    
    i) GFS0P25
    ii) GFS0P25 SECONDARY PARAMETERS
    iii) GEFS0P25
    iv) GEFS0P50
    v) GEFS0P50 SECONDARY PARAMETERS

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

    try:
        aa, bb = url_index(model, directory)
    except Exception as e:
        print(f"{directory} is not a valid directory for {model}.")
        sys.exit(1)
    
    if model == 'GFS0P25' or model == 'GFS0P25 SECONDARY PARAMETERS':
        if directory == 'wave':
            folder = 'gridded'
        else:
            folder=''
        today_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/00/{directory}/{folder}"
        today_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/06/{directory}/{folder}"
        today_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/12/{directory}/{folder}"
        today_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/18/{directory}/{folder}"
        
        yday_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/00/{directory}/{folder}"
        yday_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/06/{directory}/{folder}"
        yday_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/12/{directory}/{folder}"
        yday_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/18/{directory}/{folder}"
        
        if model == 'GFS0P25':
            f_00z = f"gfs.t00z.pgrb2.0p25.f384"
            f_06z = f"gfs.t06z.pgrb2.0p25.f384"
            f_12z = f"gfs.t12z.pgrb2.0p25.f384"
            f_18z = f"gfs.t18z.pgrb2.0p25.f384"
        else:
            f_00z = f"gfs.t00z.pgrb2b.0p25.f384"
            f_06z = f"gfs.t06z.pgrb2b.0p25.f384"
            f_12z = f"gfs.t12z.pgrb2b.0p25.f384"
            f_18z = f"gfs.t18z.pgrb2b.0p25.f384"
    
    if model == 'GEFS0P25' or model == 'GEFS0P50' or model == 'GEFS0P50 SECONDARY PARAMETERS':
        
        if directory != 'wave':
            if model == 'GEFS0P25':
                
                    if directory == 'atmos':
                        a = 's'
                    else:
                        a = 'a'
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
                
            folder = f"pgrb2{a}p{b}"
        else:
            if model == 'GEFS0P25':
                c = '25'
            if model == 'GEFS0P50' or model == 'GEFS0P50 SECONDARY PARAMETERS':
                c = '50'
            folder = 'gridded'

        today_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/00/{directory}/{folder}/"
        today_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/06/{directory}/{folder}/"
        today_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/12/{directory}/{folder}/"
        today_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/18/{directory}/{folder}/"
        
        yday_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/00/{directory}/{folder}/"
        yday_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/06/{directory}/{folder}/"
        yday_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/12/{directory}/{folder}/"
        yday_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/18/{directory}/{folder}/"
    
        if directory == 'atmos':
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
        elif directory == 'chem':
            f_00z = f"gefs.chem.t00z.a2d_0p25.f120.grib2"    
            f_06z = f"gefs.chem.t06z.a2d_0p25.f120.grib2"  
            f_12z = f"gefs.chem.t12z.a2d_0p25.f120.grib2"  
            f_18z = f"gefs.chem.t18z.a2d_0p25.f120.grib2"   
        else:
            if cat == 'MEAN' or cat == 'SPREAD':
                f_00z = f"gefs.wave.t00z.{cat.lower()}.global.0p{c}.f384.grib2"  
                f_06z = f"gefs.wave.t06z.{cat.lower()}.global.0p{c}.f384.grib2"  
                f_12z = f"gefs.wave.t12z.{cat.lower()}.global.0p{c}.f384.grib2"  
                f_18z = f"gefs.wave.t18z.{cat.lower()}.global.0p{c}.f384.grib2"  
            if cat == 'CONTROL':
                f_00z = f"gefs.wave.t00z.c00.global.0p{c}.f384.grib2"  
                f_06z = f"gefs.wave.t06z.c00.global.0p{c}.f384.grib2"  
                f_12z = f"gefs.wave.t12z.c00.global.0p{c}.f384.grib2"  
                f_18z = f"gefs.wave.t18z.c00.global.0p{c}.f384.grib2"  
            if cat == 'ALL MEMBERS':
                f_00z = f"gefs.wave.t00z.p30.global.0p{c}.f384.grib2"  
                f_06z = f"gefs.wave.t06z.p30.global.0p{c}.f384.grib2"  
                f_12z = f"gefs.wave.t12z.p30.global.0p{c}.f384.grib2"  
                f_18z = f"gefs.wave.t18z.p30.global.0p{c}.f384.grib2"     
                                         
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
        
    return url, url_run


def rtma_url_scanner(model, cat, proxies):
    
    """
    This function scans for the latest available RTMA Dataset within the past 4 hours.
    
    Required Arguments:
    
    1) model (String) - The RTMA Model:
    
    RTMA Models:
    i) RTMA - CONUS
    ii) AK RTMA - Alaska
    iii) HI RTMA - Hawaii
    iv) GU RTMA - Guam
    v) PR RTMA - Puerto Rico
    
    2) cat (String) - The category of the variables. 
    
    i) Analysis
    ii) Error
    iii) Forecast
    
    3) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                        }
    
    Returns
    -------
    
    The URL path to the file and the filename for the most recent RTMA Dataset.
    
    """
    
    model = model.upper()
    cat = cat.upper()
    
    if model == 'RTMA':
        directory = 'rtma2p5'
    elif model == 'AK RTMA':
        directory = 'akrtma'
    elif model == 'HI RTMA':
        directory = 'hirtma'
    elif model == 'GU RTMA':
        directory = 'gurtma'
    else:
        directory = 'prrtma'
          
    if cat == 'ANALYSIS':
        f_cat = 'anl'
    elif cat == 'ERROR':
        f_cat = 'err'
    else:
        f_cat = 'ges'
            
    h_00 = now
    h_01 = now - timedelta(hours=1)
    h_02 = now - timedelta(hours=2)
    h_03 = now - timedelta(hours=3)
    h_04 = now - timedelta(hours=4)
            
    url_00 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{h_00.strftime('%Y%m%d')}/"    
    url_01 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{h_01.strftime('%Y%m%d')}/" 
    url_02 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{h_02.strftime('%Y%m%d')}/"  
    url_03 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{h_03.strftime('%Y%m%d')}/"  
    url_04 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{h_04.strftime('%Y%m%d')}/"  
    
    
    if model == 'AK RTMA':
        f_00 = f"{directory}.t{h_00.hour}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_01 = f"{directory}.t{h_01.hour}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_02 = f"{directory}.t{h_02.hour}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_03 = f"{directory}.t{h_03.hour}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_04 = f"{directory}.t{h_04.hour}z.2dvar{f_cat}_ndfd_3p0.grb2"
    
    elif model == 'RTMA':
        f_00 = f"{directory}.t{h_00.hour}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_01 = f"{directory}.t{h_01.hour}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_02 = f"{directory}.t{h_02.hour}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_03 = f"{directory}.t{h_03.hour}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_04 = f"{directory}.t{h_04.hour}z.2dvar{f_cat}_ndfd.grb2_wexp"
        
    else:
        f_00 = f"{directory}.t{h_00.hour}z.2dvar{f_cat}_ndfd.grb2"
        f_01 = f"{directory}.t{h_01.hour}z.2dvar{f_cat}_ndfd.grb2"
        f_02 = f"{directory}.t{h_02.hour}z.2dvar{f_cat}_ndfd.grb2"
        f_03 = f"{directory}.t{h_03.hour}z.2dvar{f_cat}_ndfd.grb2"
        f_04 = f"{directory}.t{h_04.hour}z.2dvar{f_cat}_ndfd.grb2"
    
    if proxies == None:
        r0 = requests.get(f"{url_00}/{f_00}", stream=True)
        r1 = requests.get(f"{url_01}/{f_01}", stream=True)
        r2 = requests.get(f"{url_02}/{f_02}", stream=True)
        r3 = requests.get(f"{url_03}/{f_03}", stream=True)
        r4 = requests.get(f"{url_04}/{f_04}", stream=True)
        
    else:
        r0 = requests.get(f"{url_00}/{f_00}", stream=True, proxies=proxies)
        r1 = requests.get(f"{url_01}/{f_01}", stream=True, proxies=proxies)
        r2 = requests.get(f"{url_02}/{f_02}", stream=True, proxies=proxies)
        r3 = requests.get(f"{url_03}/{f_03}", stream=True, proxies=proxies)
        r4 = requests.get(f"{url_04}/{f_04}", stream=True, proxies=proxies)
        
    if r0.status_code == 200:
        url = url_00
        fname = f_00
    elif r0.status_code != 200 and r1.status_code == 200:
        url = url_01
        fname = f_01  
    elif r1.status_code != 200 and r2.status_code == 200:
        url = url_02
        fname = f_02
    elif r2.status_code != 200 and r3.status_code == 200:
        url = url_03
        fname = f_03
    elif r3.status_code != 200 and r4.status_code == 200:
        url = url_04
        fname = f_04
    else:
        print(f"The latest file available is over 4 hours old. Aborting...")
        sys.exit()
        
    return url, fname                

