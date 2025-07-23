"""
This file has the scanner function which scans the data server for the latest FULL dataset and returns the download url

(C) Eric J. Drewitz 
"""

# Imports the needed packages
import requests

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

# Gets yesterday's date
yd = now - timedelta(days=1)

def scanner(data, proxies):

    """
    This function scans a webpage for the file with the latest forecast model run. 
    If the page has complete data, the download link will be returned. 
    If the page is incomplete, the scanner will check for the previous run data. 
    This scanner is used so the user downloads the latest FULL dataset. 

    Required Arguments: 

    1) data (String) - The data the user wants. 

    2) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                        }

    Returns
    -------

    The download link
    """
    if data == 'obs':
        
        cat = f"https://thredds.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.html"
        files = []
        for i in range(0, 25):
            time = now - timedelta(hours=i)
            file = f"metar_{time.strftime('%Y%m%d_%H00')}.txt"
            files.append(file)

        for f in range(0, len(files), 1):
            response = requests.get(f"{cat}/{files[f]}")
            print(response)

    if data == 'GEFS0p25 Ensemble Mean':

        today_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/00/atmos/pgrb2sp25/"
        today_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/06/atmos/pgrb2sp25/"
        today_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/12/atmos/pgrb2sp25/"
        today_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/18/atmos/pgrb2sp25/"
        
        yday_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/00/atmos/pgrb2sp25/"
        yday_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/06/atmos/pgrb2sp25/"
        yday_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/12/atmos/pgrb2sp25/"
        yday_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/18/atmos/pgrb2sp25/"

        f_00z = f"geavg.t00z.pgrb2s.0p25.f240"
        f_06z = f"geavg.t06z.pgrb2s.0p25.f240"
        f_12z = f"geavg.t12z.pgrb2s.0p25.f240"
        f_18z = f"geavg.t18z.pgrb2s.0p25.f240"

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
            url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/18/atmos/pgrb2sp25/"
        elif t_18z.status_code != 200 and t_12z.status_code == 200:
            url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/12/atmos/pgrb2sp25/"
        elif t_12z.status_code != 200 and t_06z.status_code == 200:
            url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/06/atmos/pgrb2sp25/"        
        elif t_06z.status_code != 200 and t_00z.status_code == 200:
            url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/00/atmos/pgrb2sp25/" 
        elif t_00z.status_code != 200 and y_18z.status_code == 200:
            url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/18/atmos/pgrb2sp25/"
        elif y_18z.status_code != 200 and y_12z.status_code == 200:
            url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/12/atmos/pgrb2sp25/"        
        elif y_12z.status_code != 200 and y_06z.status_code == 200:
            url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/06/atmos/pgrb2sp25/" 
        else:
            url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/00/atmos/pgrb2sp25/"


    return url
