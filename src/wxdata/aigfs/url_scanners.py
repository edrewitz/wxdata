"""
This file hosts the URL Scanner for the AIGFS

(C) Eric J. Drewitz 2025
"""

import requests
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

def aigfs_url_scanner(final_forecast_hour,
                                    proxies,
                                    type_of_level):
    
    """
    This function is the URL scanner for the AIGFS Data.
    
    This function returns the URL and filename of the latest available AIGEFS Pressure data on the NCEP NOMADS Server. 
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. 
       The AIGFS goes out 384 hours.
       
    2) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
                        
    3) type_of_level (String) - The type of level the data is in.
    
        Types of Levels
        ---------------
        
        1) pressure
        2) surface
        
    
    Optional Arguments: None
    
    Returns
    -------
    
    The download URL and filename of the latest available file in the AIGEFS dataset.  
    """

    type_of_level = type_of_level.lower()
        
    if type_of_level == 'pressure':
        level = 'pres'
    else:
        level = 'sfc'
    
    if final_forecast_hour > 384:
        print(f"User's input value of {final_forecast_hour} is beyond the period.\nDefaulting to hour 384.")
        final_forecast_hour = 384
    else:
        final_forecast_hour = final_forecast_hour
        
    if final_forecast_hour >= 100:
        final_forecast_hour = f"{final_forecast_hour}"
    elif final_forecast_hour >= 10 and final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = f"00{final_forecast_hour}"
        
    today_18z_url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/aigfs/para/aigfs.{now.strftime('%Y%m%d')}/18/model/atmos/grib2/"
    today_12z_url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/aigfs/para/aigfs.{now.strftime('%Y%m%d')}/12/model/atmos/grib2/"
    today_06z_url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/aigfs/para/aigfs.{now.strftime('%Y%m%d')}/06/model/atmos/grib2/"
    today_00z_url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/aigfs/para/aigfs.{now.strftime('%Y%m%d')}/00/model/atmos/grib2/"
    
    yesterday_18z_url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/aigfs/para/aigfs.{yd.strftime('%Y%m%d')}/18/model/atmos/grib2/"
    yesterday_12z_url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/aigfs/para/aigfs.{yd.strftime('%Y%m%d')}/12/model/atmos/grib2/"
    yesterday_06z_url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/aigfs/para/aigfs.{yd.strftime('%Y%m%d')}/06/model/atmos/grib2/"
    yesterday_00z_url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/aigfs/para/aigfs.{yd.strftime('%Y%m%d')}/00/model/atmos/grib2/"

                
    file_18z = f"aigfs.t18z.{level}.f{final_forecast_hour}.grib2"
    file_12z = f"aigfs.t12z.{level}.f{final_forecast_hour}.grib2"
    file_06z = f"aigfs.t06z.{level}.f{final_forecast_hour}.grib2"
    file_00z = f"aigfs.t00z.{level}.f{final_forecast_hour}.grib2"
    
    if proxies == None:
        try:    
            t_18 = requests.get(f"{today_18z_url}/{file_18z}", stream=True)
            t_18.close()
            t_12 = requests.get(f"{today_12z_url}/{file_12z}", stream=True)
            t_12.close()
            t_06 = requests.get(f"{today_06z_url}/{file_06z}", stream=True)
            t_06.close()
            t_00 = requests.get(f"{today_00z_url}/{file_00z}", stream=True)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_url}/{file_18z}", stream=True)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_url}/{file_12z}", stream=True)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_url}/{file_06z}", stream=True)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_url}/{file_00z}", stream=True)
            y_00.close()
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_url}/{file_18z}", stream=True)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_url}/{file_12z}", stream=True)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_url}/{file_06z}", stream=True)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_url}/{file_00z}", stream=True)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_url}/{file_18z}", stream=True)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_url}/{file_12z}", stream=True)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_url}/{file_06z}", stream=True)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_url}/{file_00z}", stream=True)
                    y_00.close()
                    break
                except Exception as e:
                    i = i     
                    
                       
    else:
        try:    
            t_18 = requests.get(f"{today_18z_url}/{file_18z}", stream=True, proxies=proxies)
            t_18.close()
            t_12 = requests.get(f"{today_12z_url}/{file_12z}", stream=True, proxies=proxies)
            t_12.close()
            t_06 = requests.get(f"{today_06z_url}/{file_06z}", stream=True, proxies=proxies)
            t_06.close()
            t_00 = requests.get(f"{today_00z_url}/{file_00z}", stream=True, proxies=proxies)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_url}/{file_18z}", stream=True, proxies=proxies)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_url}/{file_12z}", stream=True, proxies=proxies)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_url}/{file_06z}", stream=True, proxies=proxies)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_url}/{file_00z}", stream=True, proxies=proxies)
            y_00.close()
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_url}/{file_18z}", stream=True, proxies=proxies)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_url}/{file_12z}", stream=True, proxies=proxies)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_url}/{file_06z}", stream=True, proxies=proxies)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_url}/{file_00z}", stream=True, proxies=proxies)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_url}/{file_18z}", stream=True, proxies=proxies)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_url}/{file_12z}", stream=True, proxies=proxies)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_url}/{file_06z}", stream=True, proxies=proxies)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_url}/{file_00z}", stream=True, proxies=proxies)
                    y_00.close()
                    break
                except Exception as e:
                    i = i 
                    
                    
    urls = [
        today_18z_url,
        today_12z_url,
        today_06z_url,
        today_00z_url,
        yesterday_18z_url,
        yesterday_12z_url,
        yesterday_06z_url,
        yesterday_00z_url
        
    ]
    
    responses = [
        t_18,
        t_12,
        t_06,
        t_00,
        y_18,
        y_12,
        y_06,
        y_00
    ]
    
    # Testing the status code and then returning the first link with a status code of 200
    for response, url in zip(responses, urls):
        if response.status_code == 200:
            url = url
            run = int(f"{url[-21]}{url[-20]}")
            if run < 10:
                file = f"aigfs.t0{run}z.{level}.f{final_forecast_hour}.grib2"
            else:
                file = f"aigfs.t{run}z.{level}.f{final_forecast_hour}.grib2"
            break   
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
        
    return url, file, run