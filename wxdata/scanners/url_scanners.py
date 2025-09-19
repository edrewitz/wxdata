"""
This file hosts all the URL Scanner Functions.

These functions return the URL and filename for the latest available data on the dataservers.

(C) Eric J. Drewitz 2025
"""

import requests
import sys

from wxdata.scanners.keys import *
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

def gem_global_scanner(final_forecast_hour, proxies):
    
    """
    This function scans https://dd.weather.gc.ca/ for the file with the latest GEM Global run. 
    
    If the page has complete data, the download link will be returned. 
    If the page is incomplete, the scanner will check for the previous run data.  
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - Default = 240. The final forecast hour the user wishes to download. The GEM Global
    goes out to 240 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    2) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                        }
    
    Optional Arguments: None
    
                        
    Returns
    -------

    1) The download link.
    2) The time of the latest model run. 
    3) The date of the run in the form of a string
    """
    
    if final_forecast_hour < 10:
        final_forecast_hour = f"00{final_forecast_hour}"
    elif final_forecast_hour >= 10 and final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = f"{final_forecast_hour}"
        
    
    f_today_00z = f"CMC_glb_ABSV_ISBL_200_latlon.15x.15_{now.strftime('%Y%m%d')}00_P{final_forecast_hour}.grib2"
    f_today_12z = f"CMC_glb_ABSV_ISBL_200_latlon.15x.15_{now.strftime('%Y%m%d')}12_P{final_forecast_hour}.grib2"
    f_yday_00z = f"CMC_glb_ABSV_ISBL_200_latlon.15x.15_{yd.strftime('%Y%m%d')}00_P{final_forecast_hour}.grib2"
    f_yday_12z = f"CMC_glb_ABSV_ISBL_200_latlon.15x.15_{yd.strftime('%Y%m%d')}12_P{final_forecast_hour}.grib2"

    
    url_today_00z = f"https://dd.weather.gc.ca/{now.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/00/{final_forecast_hour}/"
    url_today_12z = f"https://dd.weather.gc.ca/{now.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/12/{final_forecast_hour}/"
    url_yday_00z = f"https://dd.weather.gc.ca/{yd.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/00/{final_forecast_hour}/"
    url_yday_12z = f"https://dd.weather.gc.ca/{yd.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/12/{final_forecast_hour}/"
    
    download_url_t_00z = f"https://dd.weather.gc.ca/{now.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/00/"
    download_url_t_12z = f"https://dd.weather.gc.ca/{now.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/12/"
    download_url_y_00z = f"https://dd.weather.gc.ca/{yd.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/00/"
    download_url_y_12z = f"https://dd.weather.gc.ca/{yd.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/12/"
    
    if proxies == None:
        t_12z = requests.get(f"{url_today_12z}/{f_today_12z}", stream=True)
        t_00z = requests.get(f"{url_today_00z}/{f_today_00z}", stream=True)
        y_12z = requests.get(f"{url_yday_12z}/{f_yday_12z}", stream=True)
        y_00z = requests.get(f"{url_yday_00z}/{f_yday_00z}", stream=True)
    else:
        t_12z = requests.get(f"{url_today_12z}/{f_today_12z}", stream=True, proxies=proxies)
        t_00z = requests.get(f"{url_today_00z}/{f_today_00z}", stream=True, proxies=proxies)
        y_12z = requests.get(f"{url_yday_12z}/{f_yday_12z}", stream=True, proxies=proxies)
        y_00z = requests.get(f"{url_yday_00z}/{f_yday_00z}", stream=True, proxies=proxies)       
    
    if t_12z.status_code == 200:
        url = download_url_t_12z
        run = '12'
        date =f"{now.strftime('%Y%m%d')}"
    elif t_12z.status_code != 200 and t_00z.status_code == 200:
        url = download_url_t_00z
        run = '00'        
        date =f"{now.strftime('%Y%m%d')}"
    elif t_12z.status_code != 200 and t_00z.status_code != 200 and y_12z.status_code == 200:
        url = download_url_y_12z
        run = '12'
        date =f"{yd.strftime('%Y%m%d')}"
    else:
        url = download_url_y_00z
        run = '00'
        date =f"{yd.strftime('%Y%m%d')}"
        
    return url, run, date
    



def gfs_url_scanner(model, cat, proxies, directory, final_forecast_hour, members=None):

    """
    This function scans https://nomads.ncep.noaa.gov/ for the file with the latest GFS/GEFS forecast model run. 
    If the page has complete data, the download link will be returned. 
    If the page is incomplete, the scanner will check for the previous run data.  

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
                    
    5) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    Optional Arguments: 
    
    1) members (Integer) - Default = None. An array of integers corresponding to the last (highest number) ensemble member in the 
    datast which the user wishes to download. 

    Returns
    -------

    1) The download link.
    2) The time of the latest model run. 
    """
    model = model.upper()
    cat = cat.upper()
    directory = directory.lower()
    
    if members != None:
        member = members[-1]
        if member < 10:
            member = f"0{member}"
        elif member >= 10:
            member = f"{member}"
        else:
            member = f"30"
    else:
        pass
    
    if model == 'GEFS0P25' and final_forecast_hour > 240:
        final_forecast_hour = 240
    
    if directory == 'chem' and final_forecast_hour >= 120:
        final_forecast_hour = 120
        
    if final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = final_forecast_hour

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
            f_00z = f"gfs.t00z.pgrb2.0p25.f{final_forecast_hour}"
            f_06z = f"gfs.t06z.pgrb2.0p25.f{final_forecast_hour}"
            f_12z = f"gfs.t12z.pgrb2.0p25.f{final_forecast_hour}"
            f_18z = f"gfs.t18z.pgrb2.0p25.f{final_forecast_hour}"
        else:
            f_00z = f"gfs.t00z.pgrb2b.0p25.f{final_forecast_hour}"
            f_06z = f"gfs.t06z.pgrb2b.0p25.f{final_forecast_hour}"
            f_12z = f"gfs.t12z.pgrb2b.0p25.f{final_forecast_hour}"
            f_18z = f"gfs.t18z.pgrb2b.0p25.f{final_forecast_hour}"
    
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
                    f_00z = f"gec00.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_06z = f"gec00.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_12z = f"gec00.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_18z = f"gec00.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}" 
                elif model == 'GEFS0P50':
                    f_00z = f"geavg.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_06z = f"geavg.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_12z = f"geavg.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_18z = f"geavg.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}"                
                else:
                    f_00z = f"geavg.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_06z = f"geavg.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_12z = f"geavg.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_18z = f"geavg.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
            elif cat == 'CONTROL':
                if model == 'GEFS0P25':
                    f_00z = f"gec00.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_06z = f"gec00.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_12z = f"gec00.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_18z = f"gec00.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}" 
                else:
                    f_00z = f"gec00.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_06z = f"gec00.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_12z = f"gec00.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_18z = f"gec00.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}"                      
            else:
                if model == 'GEFS0P25':
                    f_00z = f"gep{member}.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_06z = f"gep{member}.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_12z = f"gep{member}.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_18z = f"gep{member}.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}"   
                else:
                    f_00z = f"gep{member}.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_06z = f"gep{member}.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_12z = f"gep{member}.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                    f_18z = f"gep{member}.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}"                         
        elif directory == 'chem':
            if model == 'GEFS0P25':
                f_00z = f"gefs.chem.t00z.a2d_0p{c}.f{final_forecast_hour}.grib2"    
                f_06z = f"gefs.chem.t06z.a2d_0p{c}.f{final_forecast_hour}.grib2"  
                f_12z = f"gefs.chem.t12z.a2d_0p{c}.f{final_forecast_hour}.grib2"  
                f_18z = f"gefs.chem.t18z.a2d_0p{c}.f{final_forecast_hour}.grib2"   
            else:
                f_00z = f"gefs.chem.t00z.a3d_0p{c}.f{final_forecast_hour}.grib2"    
                f_06z = f"gefs.chem.t06z.a3d_0p{c}.f{final_forecast_hour}.grib2"  
                f_12z = f"gefs.chem.t12z.a3d_0p{c}.f{final_forecast_hour}.grib2"  
                f_18z = f"gefs.chem.t18z.a3d_0p{c}.f{final_forecast_hour}.grib2"   
        else:
            if cat == 'MEAN' or cat == 'SPREAD' or cat == 'PROB':
                f_00z = f"gefs.wave.t00z.{cat.lower()}.global.0p{c}.f{final_forecast_hour}.grib2"  
                f_06z = f"gefs.wave.t06z.{cat.lower()}.global.0p{c}.f{final_forecast_hour}.grib2"  
                f_12z = f"gefs.wave.t12z.{cat.lower()}.global.0p{c}.f{final_forecast_hour}.grib2"  
                f_18z = f"gefs.wave.t18z.{cat.lower()}.global.0p{c}.f{final_forecast_hour}.grib2"  
            elif cat == 'CONTROL':
                f_00z = f"gefs.wave.t00z.c00.global.0p{c}.f{final_forecast_hour}.grib2"  
                f_06z = f"gefs.wave.t06z.c00.global.0p{c}.f{final_forecast_hour}.grib2"  
                f_12z = f"gefs.wave.t12z.c00.global.0p{c}.f{final_forecast_hour}.grib2"  
                f_18z = f"gefs.wave.t18z.c00.global.0p{c}.f{final_forecast_hour}.grib2"  
            else:
                f_00z = f"gefs.wave.t00z.p{member}.global.0p{c}.f{final_forecast_hour}.grib2"  
                f_06z = f"gefs.wave.t06z.p{member}.global.0p{c}.f{final_forecast_hour}.grib2"  
                f_12z = f"gefs.wave.t12z.p{member}.global.0p{c}.f{final_forecast_hour}.grib2"  
                f_18z = f"gefs.wave.t18z.p{member}.global.0p{c}.f{final_forecast_hour}.grib2"     
                                         
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
