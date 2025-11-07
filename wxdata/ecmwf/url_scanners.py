"""
This file hosts the ECMWF URL Scanner Functions.

These functions return the URL and filename for the latest available data on the ECMWF dataservers.

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


def ecmwf_ifs_url_scanner(final_forecast_hour,
                          proxies):
    
    """
    This function scans for the URL of the latest available ECMWF IFS data on the ECMWF Data Store. 
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The ECMWF IFS
    goes out to 360 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    360 by the nereast increment of 3 hours. 
    
    2) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
    
    Returns
    -------
    
    The download URL and filename of the latest file in the ECMWF IFS dataset.   
    The ECMWF Data Store Server Status Code. 
    """
    
    if final_forecast_hour > 360:
        print("""
              ERROR: The ECMWF IFS goes out to 360 hours. 
              You entered a final_forecast_hour > 360. 
              Defaulting to 360 as the final_forecast_hour.  
              """)
        
        final_forecast_hour = 360
        
    else:
        final_forecast_hour = final_forecast_hour
        
    today_12z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/12z/ifs/0p25/oper/"
    today_00z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/00z/ifs/0p25/oper/"
    yesterday_12z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/12z/ifs/0p25/oper/"
    yesterday_00z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/00z/ifs/0p25/oper/"
    
    file_12z_today = f"{now.strftime('%Y%m%d')}120000-{final_forecast_hour}h-oper-fc.grib2"
    file_00z_today = f"{now.strftime('%Y%m%d')}000000-{final_forecast_hour}h-oper-fc.grib2"
    file_12z_yesterday = f"{yd.strftime('%Y%m%d')}120000-{final_forecast_hour}h-oper-fc.grib2"
    file_00z_yesterday = f"{yd.strftime('%Y%m%d')}000000-{final_forecast_hour}h-oper-fc.grib2"
    
    if proxies == None:
        try:
            t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True)
            t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True)
            y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True)
            y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True)
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(30)
                try:
                    t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True)
                    t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True)
                    y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True)
                    y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True)
                    break
                except Exception as e:
                    i = i
        
    else:
        try:
            t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True, proxies=proxies)
            t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True, proxies=proxies)
            y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True, proxies=proxies)
            y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True, proxies=proxies)
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(30)
                try:
                    t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True, proxies=proxies)
                    t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True, proxies=proxies)
                    y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True, proxies=proxies)
                    y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True, proxies=proxies)
                    break
                except Exception as e:
                    i = i
        
    urls = [
        today_12z_url,
        today_00z_url,
        yesterday_12z_url,
        yesterday_00z_url
        
    ]
    
    responses = [
        t_12,
        t_00,
        y_12,
        y_00
    ]
    
    files = [
        file_12z_today,
        file_00z_today,
        file_12z_yesterday,
        file_00z_yesterday
    ]
    
    # Testing the status code and then returning the first link with a status code of 200

    for response, url, file in zip(responses, urls, files):
        if response.status_code == 200:
            url = url
            file = file
            run = int(f"{file[8]}{file[9]}")
            break        
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
        
    return url, file, run


def ecmwf_aifs_url_scanner(final_forecast_hour,
                          proxies):
    
    """
    This function scans for the URL of the latest available ECMWF AIFS data on the ECMWF Data Store. 
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The ECMWF AIFS
    goes out to 360 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    360 by the nereast increment of 3 hours. 
    
    2) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
    
    
    Returns
    -------
    
    The download URL and filename of the latest file in the ECMWF AIFS dataset.  
    The ECMWF Data Store Server Status Code.       
    """
    
    if final_forecast_hour > 360:
        print("""
              ERROR: The ECMWF AIFS goes out to 360 hours. 
              You entered a final_forecast_hour > 360. 
              Defaulting to 360 as the final_forecast_hour.  
              """)
        
        final_forecast_hour = 360
        
    else:
        final_forecast_hour = final_forecast_hour
        
    today_18z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/18z/aifs-single/0p25/oper/"
    today_12z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/12z/aifs-single/0p25/oper/"
    today_06z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/06z/aifs-single/0p25/oper/"
    today_00z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/00z/aifs-single/0p25/oper/"
    yesterday_18z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/18z/aifs-single/0p25/oper/"
    yesterday_12z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/12z/aifs-single/0p25/oper/"
    yesterday_06z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/06z/aifs-single/0p25/oper/"
    yesterday_00z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/00z/aifs-single/0p25/oper/"
    
    file_18z_today = f"{now.strftime('%Y%m%d')}180000-{final_forecast_hour}h-oper-fc.grib2"
    file_12z_today = f"{now.strftime('%Y%m%d')}120000-{final_forecast_hour}h-oper-fc.grib2"
    file_06z_today = f"{now.strftime('%Y%m%d')}060000-{final_forecast_hour}h-oper-fc.grib2"
    file_00z_today = f"{now.strftime('%Y%m%d')}000000-{final_forecast_hour}h-oper-fc.grib2"
    file_18z_yesterday = f"{yd.strftime('%Y%m%d')}180000-{final_forecast_hour}h-oper-fc.grib2"
    file_12z_yesterday = f"{yd.strftime('%Y%m%d')}120000-{final_forecast_hour}h-oper-fc.grib2"
    file_06z_yesterday = f"{yd.strftime('%Y%m%d')}060000-{final_forecast_hour}h-oper-fc.grib2"
    file_00z_yesterday = f"{yd.strftime('%Y%m%d')}000000-{final_forecast_hour}h-oper-fc.grib2"
    
    if proxies == None:
        try:    
            t_18 = requests.get(f"{today_18z_url}/{file_18z_today}", stream=True)
            t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True)
            t_06 = requests.get(f"{today_06z_url}/{file_06z_today}", stream=True)
            t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True)
            y_18 = requests.get(f"{yesterday_18z_url}/{file_18z_yesterday}", stream=True)
            y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True)
            y_06 = requests.get(f"{yesterday_06z_url}/{file_06z_yesterday}", stream=True)
            y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True)
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_url}/{file_18z_today}", stream=True)
                    t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True)
                    t_06 = requests.get(f"{today_06z_url}/{file_06z_today}", stream=True)
                    t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True)
                    y_18 = requests.get(f"{yesterday_18z_url}/{file_18z_yesterday}", stream=True)
                    y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True)
                    y_06 = requests.get(f"{yesterday_06z_url}/{file_06z_yesterday}", stream=True)
                    y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True)
                    break
                except Exception as e:
                    i = i                    
    else:
        try:
            t_18 = requests.get(f"{today_18z_url}/{file_18z_today}", stream=True, proxies=proxies)
            t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True, proxies=proxies)
            t_06 = requests.get(f"{today_06z_url}/{file_06z_today}", stream=True, proxies=proxies)
            t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True, proxies=proxies)
            y_18 = requests.get(f"{yesterday_18z_url}/{file_18z_yesterday}", stream=True, proxies=proxies)
            y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True, proxies=proxies)
            y_06 = requests.get(f"{yesterday_06z_url}/{file_06z_yesterday}", stream=True, proxies=proxies)
            y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True, proxies=proxies)
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_url}/{file_18z_today}", stream=True, proxies=proxies)
                    t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True, proxies=proxies)
                    t_06 = requests.get(f"{today_06z_url}/{file_06z_today}", stream=True, proxies=proxies)
                    t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True, proxies=proxies)
                    y_18 = requests.get(f"{yesterday_18z_url}/{file_18z_yesterday}", stream=True, proxies=proxies)
                    y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True, proxies=proxies)
                    y_06 = requests.get(f"{yesterday_06z_url}/{file_06z_yesterday}", stream=True, proxies=proxies)
                    y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True, proxies=proxies)   
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
    
    files = [
        file_18z_today,
        file_12z_today,
        file_06z_today,
        file_00z_today,
        file_18z_yesterday,
        file_12z_yesterday,
        file_06z_yesterday,
        file_00z_yesterday
    ]
    
    # Testing the status code and then returning the first link with a status code of 200
    for response, url, file in zip(responses, urls, files):
        if response.status_code == 200:
            url = url
            file = file
            run = int(f"{file[8]}{file[9]}")
            break        
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
        
    return url, file, run

def ecmwf_ifs_high_res_url_scanner(final_forecast_hour,
                          proxies):
    
    """
    This function scans for the URL of the latest available ECMWF High Resolution IFS data on the ECMWF Data Store. 
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The ECMWF High Resolution IFS
    goes out to 144 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    144 by the nereast increment of 3 hours. 
    
    2) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
    
    Returns
    -------
    
    The download URL and filename of the latest file in the ECMWF High Resolution IFS dataset.    
    The ECMWF Data Store Server Status Code. 
    """
    
    if final_forecast_hour > 144:
        print("""
              ERROR: The ECMWF High Resolution IFS goes out to 144 hours. 
              You entered a final_forecast_hour > 144. 
              Defaulting to 144 as the final_forecast_hour.  
              """)
        
        final_forecast_hour = 144
        
    else:
        final_forecast_hour = final_forecast_hour
        
    today_18z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/18z/ifs/0p25/scda/"
    today_12z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/12z/ifs/0p25/scda/"
    today_06z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/06z/ifs/0p25/scda/"
    today_00z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/00z/ifs/0p25/scda/"
    yesterday_18z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/18z/ifs/0p25/scda/"
    yesterday_12z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/12z/ifs/0p25/scda/"
    yesterday_06z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/06z/ifs/0p25/scda/"
    yesterday_00z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/00z/ifs/0p25/scda/"
    
    file_18z_today = f"{now.strftime('%Y%m%d')}180000-{final_forecast_hour}h-scda-fc.grib2"
    file_12z_today = f"{now.strftime('%Y%m%d')}120000-{final_forecast_hour}h-scda-fc.grib2"
    file_06z_today = f"{now.strftime('%Y%m%d')}060000-{final_forecast_hour}h-scda-fc.grib2"
    file_00z_today = f"{now.strftime('%Y%m%d')}000000-{final_forecast_hour}h-scda-fc.grib2"
    file_18z_yesterday = f"{yd.strftime('%Y%m%d')}180000-{final_forecast_hour}h-scda-fc.grib2"
    file_12z_yesterday = f"{yd.strftime('%Y%m%d')}120000-{final_forecast_hour}h-scda-fc.grib2"
    file_06z_yesterday = f"{yd.strftime('%Y%m%d')}060000-{final_forecast_hour}h-scda-fc.grib2"
    file_00z_yesterday = f"{yd.strftime('%Y%m%d')}000000-{final_forecast_hour}h-scda-fc.grib2"
    
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_url}/{file_18z_today}", stream=True)
            t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True)
            t_06 = requests.get(f"{today_06z_url}/{file_06z_today}", stream=True)
            t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True)
            y_18 = requests.get(f"{yesterday_18z_url}/{file_18z_yesterday}", stream=True)
            y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True)
            y_06 = requests.get(f"{yesterday_06z_url}/{file_06z_yesterday}", stream=True)
            y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True)
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_url}/{file_18z_today}", stream=True)
                    t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True)
                    t_06 = requests.get(f"{today_06z_url}/{file_06z_today}", stream=True)
                    t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True)
                    y_18 = requests.get(f"{yesterday_18z_url}/{file_18z_yesterday}", stream=True)
                    y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True)
                    y_06 = requests.get(f"{yesterday_06z_url}/{file_06z_yesterday}", stream=True)
                    y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True)
                    break
                except Exception as e:
                    i = i                    
        
    else:
        try:
            t_18 = requests.get(f"{today_18z_url}/{file_18z_today}", stream=True, proxies=proxies)
            t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True, proxies=proxies)
            t_06 = requests.get(f"{today_06z_url}/{file_06z_today}", stream=True, proxies=proxies)
            t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True, proxies=proxies)
            y_18 = requests.get(f"{yesterday_18z_url}/{file_18z_yesterday}", stream=True, proxies=proxies)
            y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True, proxies=proxies)
            y_06 = requests.get(f"{yesterday_06z_url}/{file_06z_yesterday}", stream=True, proxies=proxies)
            y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True, proxies=proxies)
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_url}/{file_18z_today}", stream=True, proxies=proxies)
                    t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True, proxies=proxies)
                    t_06 = requests.get(f"{today_06z_url}/{file_06z_today}", stream=True, proxies=proxies)
                    t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True, proxies=proxies)
                    y_18 = requests.get(f"{yesterday_18z_url}/{file_18z_yesterday}", stream=True, proxies=proxies)
                    y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True, proxies=proxies)
                    y_06 = requests.get(f"{yesterday_06z_url}/{file_06z_yesterday}", stream=True, proxies=proxies)
                    y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True, proxies=proxies) 
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
    
    files = [
        file_18z_today,
        file_12z_today,
        file_06z_today,
        file_00z_today,
        file_18z_yesterday,
        file_12z_yesterday,
        file_06z_yesterday,
        file_00z_yesterday
    ]
    
    # Testing the status code and then returning the first link with a status code of 200
    for response, url, file in zip(responses, urls, files):
        if response.status_code == 200:
            url = url
            file = file
            run = int(f"{file[8]}{file[9]}")
            break      
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
        
    return url, file, run

def ecmwf_ifs_wave_url_scanner(final_forecast_hour,
                          proxies):
    
    """
    This function scans for the URL of the latest available ECMWF IFS WAVE data on the ECMWF Data Store. 
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The ECMWF IFS WAVE
    goes out to 144 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    144 by the nereast increment of 3 hours. 
    
    2) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
    
    Returns
    -------
    
    The download URL and filename of the latest file in the ECMWF High Resolution IFS dataset.  
    The ECMWF Data Store Server Status Code.   
    """
    
    if final_forecast_hour > 144:
        print("""
              ERROR: The ECMWF IFS WAVE goes out to 144 hours. 
              You entered a final_forecast_hour > 144. 
              Defaulting to 144 as the final_forecast_hour.  
              """)
        
        final_forecast_hour = 144
        
    else:
        final_forecast_hour = final_forecast_hour
        
    today_18z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/18z/ifs/0p25/scwv/"
    today_12z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/12z/ifs/0p25/scwv/"
    today_06z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/06z/ifs/0p25/scwv/"
    today_00z_url = f"https://data.ecmwf.int/forecasts/{now.strftime('%Y%m%d')}/00z/ifs/0p25/scwv/"
    yesterday_18z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/18z/ifs/0p25/scwv/"
    yesterday_12z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/12z/ifs/0p25/scwv/"
    yesterday_06z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/06z/ifs/0p25/scwv/"
    yesterday_00z_url = f"https://data.ecmwf.int/forecasts/{yd.strftime('%Y%m%d')}/00z/ifs/0p25/scwv/"
    
    file_18z_today = f"{now.strftime('%Y%m%d')}180000-{final_forecast_hour}h-scwv-fc.grib2"
    file_12z_today = f"{now.strftime('%Y%m%d')}120000-{final_forecast_hour}h-scwv-fc.grib2"
    file_06z_today = f"{now.strftime('%Y%m%d')}060000-{final_forecast_hour}h-scwv-fc.grib2"
    file_00z_today = f"{now.strftime('%Y%m%d')}000000-{final_forecast_hour}h-scwv-fc.grib2"
    file_18z_yesterday = f"{yd.strftime('%Y%m%d')}180000-{final_forecast_hour}h-scwv-fc.grib2"
    file_12z_yesterday = f"{yd.strftime('%Y%m%d')}120000-{final_forecast_hour}h-scwv-fc.grib2"
    file_06z_yesterday = f"{yd.strftime('%Y%m%d')}060000-{final_forecast_hour}h-scwv-fc.grib2"
    file_00z_yesterday = f"{yd.strftime('%Y%m%d')}000000-{final_forecast_hour}h-scwv-fc.grib2"
    
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_url}/{file_18z_today}", stream=True)
            t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True)
            t_06 = requests.get(f"{today_06z_url}/{file_06z_today}", stream=True)
            t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True)
            y_18 = requests.get(f"{yesterday_18z_url}/{file_18z_yesterday}", stream=True)
            y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True)
            y_06 = requests.get(f"{yesterday_06z_url}/{file_06z_yesterday}", stream=True)
            y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True)
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_url}/{file_18z_today}", stream=True)
                    t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True)
                    t_06 = requests.get(f"{today_06z_url}/{file_06z_today}", stream=True)
                    t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True)
                    y_18 = requests.get(f"{yesterday_18z_url}/{file_18z_yesterday}", stream=True)
                    y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True)
                    y_06 = requests.get(f"{yesterday_06z_url}/{file_06z_yesterday}", stream=True)
                    y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True)   
                    break
                except Exception as e:
                    i = i             
        
    else:
        try:
            t_18 = requests.get(f"{today_18z_url}/{file_18z_today}", stream=True, proxies=proxies)
            t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True, proxies=proxies)
            t_06 = requests.get(f"{today_06z_url}/{file_06z_today}", stream=True, proxies=proxies)
            t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True, proxies=proxies)
            y_18 = requests.get(f"{yesterday_18z_url}/{file_18z_yesterday}", stream=True, proxies=proxies)
            y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True, proxies=proxies)
            y_06 = requests.get(f"{yesterday_06z_url}/{file_06z_yesterday}", stream=True, proxies=proxies)
            y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True, proxies=proxies)
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_url}/{file_18z_today}", stream=True, proxies=proxies)
                    t_12 = requests.get(f"{today_12z_url}/{file_12z_today}", stream=True, proxies=proxies)
                    t_06 = requests.get(f"{today_06z_url}/{file_06z_today}", stream=True, proxies=proxies)
                    t_00 = requests.get(f"{today_00z_url}/{file_00z_today}", stream=True, proxies=proxies)
                    y_18 = requests.get(f"{yesterday_18z_url}/{file_18z_yesterday}", stream=True, proxies=proxies)
                    y_12 = requests.get(f"{yesterday_12z_url}/{file_12z_yesterday}", stream=True, proxies=proxies)
                    y_06 = requests.get(f"{yesterday_06z_url}/{file_06z_yesterday}", stream=True, proxies=proxies)
                    y_00 = requests.get(f"{yesterday_00z_url}/{file_00z_yesterday}", stream=True, proxies=proxies)   
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
    
    files = [
        file_18z_today,
        file_12z_today,
        file_06z_today,
        file_00z_today,
        file_18z_yesterday,
        file_12z_yesterday,
        file_06z_yesterday,
        file_00z_yesterday
    ]
    
    # Testing the status code and then returning the first link with a status code of 200
    for response, url, file in zip(responses, urls, files):
        if response.status_code == 200:
            url = url
            file = file
            run = int(f"{file[8]}{file[9]}")
            break       
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
        
    return url, file, run