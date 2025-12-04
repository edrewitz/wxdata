"""
This file hosts the RTMA URL Scanner Functions.

These functions return the URL and filename for the latest available data on the dataservers.

(C) Eric J. Drewitz 2025
"""

import requests
import sys
import numpy as np

from urllib.parse import urlparse, parse_qs
from wxdata.utils.coords import convert_lon
from wxdata.rtma.keys import *

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


def rtma_url_scanner(model, 
                    cat,
                    western_bound, 
                    eastern_bound, 
                    northern_bound, 
                    southern_bound, 
                    proxies):
    
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
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                        }
    
    Returns
    -------
    
    The URL path to the file and the filename for the most recent RTMA Dataset.
    
    """
    model = model.upper()
    cat = cat.upper()
    
    western_bound, eastern_bound = convert_lon(western_bound, eastern_bound)
    
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
    
    if h_00.hour < 10:
        abbrev_0 = f"t0{h_00.hour}"
    else:
        abbrev_0 = f"t{h_00.hour}" 
    if h_01.hour < 10:
        abbrev_1 = f"t0{h_01.hour}"
    else:
        abbrev_1 = f"t{h_01.hour}" 
    if h_02.hour < 10:
        abbrev_2 = f"t0{h_02.hour}"
    else:
        abbrev_2 = f"t{h_02.hour}" 
    if h_03.hour < 10:
        abbrev_3 = f"t0{h_03.hour}"
    else:
        abbrev_3 = f"t{h_03.hour}" 
    if h_04.hour < 10:
        abbrev_4 = f"t0{h_04.hour}"
    else:
        abbrev_4 = f"t{h_04.hour}" 
    
    
    if model == 'AK RTMA':
        f_00 = f"{directory}.{abbrev_0}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_01 = f"{directory}.{abbrev_1}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_02 = f"{directory}.{abbrev_2}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_03 = f"{directory}.{abbrev_3}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_04 = f"{directory}.{abbrev_4}z.2dvar{f_cat}_ndfd_3p0.grb2"
    
    elif model == 'RTMA':
        f_00 = f"{directory}.{abbrev_0}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_01 = f"{directory}.{abbrev_1}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_02 = f"{directory}.{abbrev_2}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_03 = f"{directory}.{abbrev_3}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_04 = f"{directory}.{abbrev_4}z.2dvar{f_cat}_ndfd.grb2_wexp"
        
    else:
        f_00 = f"{directory}.{abbrev_0}z.2dvar{f_cat}_ndfd.grb2"
        f_01 = f"{directory}.{abbrev_1}z.2dvar{f_cat}_ndfd.grb2"
        f_02 = f"{directory}.{abbrev_2}z.2dvar{f_cat}_ndfd.grb2"
        f_03 = f"{directory}.{abbrev_3}z.2dvar{f_cat}_ndfd.grb2"
        f_04 = f"{directory}.{abbrev_4}z.2dvar{f_cat}_ndfd.grb2"
    
    if proxies == None:
        try:
            r0 = requests.get(f"{url_00}/{f_00}", stream=True)
            r0.close()
            r1 = requests.get(f"{url_01}/{f_01}", stream=True)
            r1.close()
            r2 = requests.get(f"{url_02}/{f_02}", stream=True)
            r2.close()
            r3 = requests.get(f"{url_03}/{f_03}", stream=True)
            r3.close()
            r4 = requests.get(f"{url_04}/{f_04}", stream=True)
            r4.close()
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    r0 = requests.get(f"{url_00}/{f_00}", stream=True)
                    r0.close()
                    r1 = requests.get(f"{url_01}/{f_01}", stream=True)
                    r1.close()
                    r2 = requests.get(f"{url_02}/{f_02}", stream=True)
                    r2.close()
                    r3 = requests.get(f"{url_03}/{f_03}", stream=True)
                    r3.close()
                    r4 = requests.get(f"{url_04}/{f_04}", stream=True)
                    r4.close()
                    break
                except Exception as e:
                    i = i                
        
    else:
        try:
            r0 = requests.get(f"{url_00}/{f_00}", stream=True, proxies=proxies)
            r0.close()
            r1 = requests.get(f"{url_01}/{f_01}", stream=True, proxies=proxies)
            r1.close()
            r2 = requests.get(f"{url_02}/{f_02}", stream=True, proxies=proxies)
            r2.close()
            r3 = requests.get(f"{url_03}/{f_03}", stream=True, proxies=proxies)
            r3.close()
            r4 = requests.get(f"{url_04}/{f_04}", stream=True, proxies=proxies)
            r4.close()
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    r0 = requests.get(f"{url_00}/{f_00}", stream=True, proxies=proxies)
                    r0.close()
                    r1 = requests.get(f"{url_01}/{f_01}", stream=True, proxies=proxies)
                    r1.close()
                    r2 = requests.get(f"{url_02}/{f_02}", stream=True, proxies=proxies)
                    r2.close()
                    r3 = requests.get(f"{url_03}/{f_03}", stream=True, proxies=proxies)
                    r3.close()
                    r4 = requests.get(f"{url_04}/{f_04}", stream=True, proxies=proxies)
                    r4.close()
                    break
                except Exception as e:
                    i = i      
        
    url_0 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{h_00.strftime('%Y%m%d')}&file={f_00}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_1 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{h_01.strftime('%Y%m%d')}&file={f_01}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_2 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{h_02.strftime('%Y%m%d')}&file={f_02}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_3 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{h_03.strftime('%Y%m%d')}&file={f_03}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_4 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{h_04.strftime('%Y%m%d')}&file={f_04}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    urls = [
        url_0,
        url_1,
        url_2,
        url_3,
        url_4
    ]
    
    responses = [
        r0,
        r1,
        r2,
        r3,
        r4
    ]
    
    for response, url in zip(responses, urls):
        if response.status_code == 200:
            url = url
            run = get_run_by_keyword(url)
            break        
    
    try:
        url = url
    except Exception as e:
        print(f"Latest analysis data is over 4 hours old. Aborting.....")
        sys.exit(1)
        
    parsed_url = urlparse(url)

    # Extract the query string
    query_string = parsed_url.query

    # Parse the query string into a dictionary of parameters
    query_params = parse_qs(query_string)

    # Access individual parameters
    filename = query_params.get('file', [''])[0] 
    
    return url, filename, run

def rtma_comparison_url_scanner(model, 
                    cat,
                    western_bound, 
                    eastern_bound, 
                    northern_bound, 
                    southern_bound, 
                    proxies,
                    hours):
    
    """
    This function scans for the latest available RTMA Dataset within the past 4 hours and the dataset from a user specified amount of hours prior to the latest available dataset. 
    
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
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                        }
                        
    8) hours (Integer) - Default=24. The amount of hours previous to the current dataset for the comparison dataset. 
    
    
    Returns
    -------
    
    The URL path to the file and the filename for the most recent RTMA Dataset and the dataset for a user specified amount of hours prior to the latest available dataset.
    
    """
    model = model.upper()
    cat = cat.upper()
    
    western_bound, eastern_bound = convert_lon(western_bound, eastern_bound)
    
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
    
    d0 = h_00 - timedelta(hours=hours)
    d1 = h_01 - timedelta(hours=hours)
    d2 = h_02 - timedelta(hours=hours)
    d3 = h_03 - timedelta(hours=hours)
    d4 = h_04 - timedelta(hours=hours)
            
    url_00 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{h_00.strftime('%Y%m%d')}/"    
    url_01 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{h_01.strftime('%Y%m%d')}/" 
    url_02 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{h_02.strftime('%Y%m%d')}/"  
    url_03 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{h_03.strftime('%Y%m%d')}/"  
    url_04 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{h_04.strftime('%Y%m%d')}/"  
    
    url_05 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{d0.strftime('%Y%m%d')}/"    
    url_06 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{d1.strftime('%Y%m%d')}/" 
    url_07 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{d2.strftime('%Y%m%d')}/"  
    url_08 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{d3.strftime('%Y%m%d')}/"  
    url_09 = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtma/prod/{directory}.{d4.strftime('%Y%m%d')}/" 
    
    if h_00.hour < 10:
        abbrev_0 = f"t0{h_00.hour}"
    else:
        abbrev_0 = f"t{h_00.hour}" 
    if h_01.hour < 10:
        abbrev_1 = f"t0{h_01.hour}"
    else:
        abbrev_1 = f"t{h_01.hour}" 
    if h_02.hour < 10:
        abbrev_2 = f"t0{h_02.hour}"
    else:
        abbrev_2 = f"t{h_02.hour}" 
    if h_03.hour < 10:
        abbrev_3 = f"t0{h_03.hour}"
    else:
        abbrev_3 = f"t{h_03.hour}" 
    if h_04.hour < 10:
        abbrev_4 = f"t0{h_04.hour}"
    else:
        abbrev_4 = f"t{h_04.hour}" 
        
    if d0.hour < 10:
        abbrev_5 = f"t0{d0.hour}"
    else:
        abbrev_5 = f"t{d0.hour}" 
    if d1.hour < 10:
        abbrev_6 = f"t0{d1.hour}"
    else:
        abbrev_6 = f"t{d1.hour}" 
    if d2.hour < 10:
        abbrev_7 = f"t0{d2.hour}"
    else:
        abbrev_7 = f"t{d2.hour}" 
    if d3.hour < 10:
        abbrev_8 = f"t0{d3.hour}"
    else:
        abbrev_8 = f"t{d3.hour}" 
    if d4.hour < 10:
        abbrev_9 = f"t0{d4.hour}"
    else:
        abbrev_9 = f"t{d4.hour}" 
    
    
    if model == 'AK RTMA':
        f_00 = f"{directory}.{abbrev_0}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_01 = f"{directory}.{abbrev_1}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_02 = f"{directory}.{abbrev_2}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_03 = f"{directory}.{abbrev_3}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_04 = f"{directory}.{abbrev_4}z.2dvar{f_cat}_ndfd_3p0.grb2"
        
        f_05 = f"{directory}.{abbrev_5}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_06 = f"{directory}.{abbrev_6}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_07 = f"{directory}.{abbrev_7}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_08 = f"{directory}.{abbrev_8}z.2dvar{f_cat}_ndfd_3p0.grb2"
        f_09 = f"{directory}.{abbrev_9}z.2dvar{f_cat}_ndfd_3p0.grb2"
    
    elif model == 'RTMA':
        f_00 = f"{directory}.{abbrev_0}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_01 = f"{directory}.{abbrev_1}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_02 = f"{directory}.{abbrev_2}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_03 = f"{directory}.{abbrev_3}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_04 = f"{directory}.{abbrev_4}z.2dvar{f_cat}_ndfd.grb2_wexp"
        
        f_05 = f"{directory}.{abbrev_5}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_06 = f"{directory}.{abbrev_6}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_07 = f"{directory}.{abbrev_7}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_08 = f"{directory}.{abbrev_8}z.2dvar{f_cat}_ndfd.grb2_wexp"
        f_09 = f"{directory}.{abbrev_9}z.2dvar{f_cat}_ndfd.grb2_wexp"
        
    else:
        f_00 = f"{directory}.{abbrev_0}z.2dvar{f_cat}_ndfd.grb2"
        f_01 = f"{directory}.{abbrev_1}z.2dvar{f_cat}_ndfd.grb2"
        f_02 = f"{directory}.{abbrev_2}z.2dvar{f_cat}_ndfd.grb2"
        f_03 = f"{directory}.{abbrev_3}z.2dvar{f_cat}_ndfd.grb2"
        f_04 = f"{directory}.{abbrev_4}z.2dvar{f_cat}_ndfd.grb2"
        
        f_05 = f"{directory}.{abbrev_5}z.2dvar{f_cat}_ndfd.grb2"
        f_06 = f"{directory}.{abbrev_6}z.2dvar{f_cat}_ndfd.grb2"
        f_07 = f"{directory}.{abbrev_7}z.2dvar{f_cat}_ndfd.grb2"
        f_08 = f"{directory}.{abbrev_8}z.2dvar{f_cat}_ndfd.grb2"
        f_09 = f"{directory}.{abbrev_9}z.2dvar{f_cat}_ndfd.grb2"
    
    if proxies == None:
        try:
            r0 = requests.get(f"{url_00}/{f_00}", stream=True)
            r0.close()
            r1 = requests.get(f"{url_01}/{f_01}", stream=True)
            r1.close()
            r2 = requests.get(f"{url_02}/{f_02}", stream=True)
            r2.close()
            r3 = requests.get(f"{url_03}/{f_03}", stream=True)
            r3.close()
            r4 = requests.get(f"{url_04}/{f_04}", stream=True)
            r4.close()
            
            r5 = requests.get(f"{url_00}/{f_00}", stream=True)
            r5.close()
            r6 = requests.get(f"{url_01}/{f_01}", stream=True)
            r6.close()
            r7 = requests.get(f"{url_02}/{f_02}", stream=True)
            r7.close()
            r8 = requests.get(f"{url_03}/{f_03}", stream=True)
            r8.close()
            r9 = requests.get(f"{url_04}/{f_04}", stream=True)
            r9.close()
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    r0 = requests.get(f"{url_00}/{f_00}", stream=True)
                    r0.close()
                    r1 = requests.get(f"{url_01}/{f_01}", stream=True)
                    r1.close()
                    r2 = requests.get(f"{url_02}/{f_02}", stream=True)
                    r2.close()
                    r3 = requests.get(f"{url_03}/{f_03}", stream=True)
                    r3.close()
                    r4 = requests.get(f"{url_04}/{f_04}", stream=True)
                    r4.close()
                    
                    r5 = requests.get(f"{url_00}/{f_00}", stream=True)
                    r5.close()
                    r6 = requests.get(f"{url_01}/{f_01}", stream=True)
                    r6.close()
                    r7 = requests.get(f"{url_02}/{f_02}", stream=True)
                    r7.close()
                    r8 = requests.get(f"{url_03}/{f_03}", stream=True)
                    r8.close()
                    r9 = requests.get(f"{url_04}/{f_04}", stream=True)
                    r9.close()
                    break
                except Exception as e:
                    i = i  
                                     
    else:
        try:
            r0 = requests.get(f"{url_00}/{f_00}", stream=True, proxies=proxies)
            r0.close()
            r1 = requests.get(f"{url_01}/{f_01}", stream=True, proxies=proxies)
            r1.close()
            r2 = requests.get(f"{url_02}/{f_02}", stream=True, proxies=proxies)
            r2.close()
            r3 = requests.get(f"{url_03}/{f_03}", stream=True, proxies=proxies)
            r3.close()
            r4 = requests.get(f"{url_04}/{f_04}", stream=True, proxies=proxies)
            r4.close()
            
            r5 = requests.get(f"{url_00}/{f_00}", stream=True, proxies=proxies)
            r5.close()
            r6 = requests.get(f"{url_01}/{f_01}", stream=True, proxies=proxies)
            r6.close()
            r7 = requests.get(f"{url_02}/{f_02}", stream=True, proxies=proxies)
            r7.close()
            r8 = requests.get(f"{url_03}/{f_03}", stream=True, proxies=proxies)
            r8.close()
            r9 = requests.get(f"{url_04}/{f_04}", stream=True, proxies=proxies)
            r9.close()
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    r0 = requests.get(f"{url_00}/{f_00}", stream=True, proxies=proxies)
                    r0.close()
                    r1 = requests.get(f"{url_01}/{f_01}", stream=True, proxies=proxies)
                    r1.close()
                    r2 = requests.get(f"{url_02}/{f_02}", stream=True, proxies=proxies)
                    r2.close()
                    r3 = requests.get(f"{url_03}/{f_03}", stream=True, proxies=proxies)
                    r3.close()
                    r4 = requests.get(f"{url_04}/{f_04}", stream=True, proxies=proxies)
                    r4.close()
                    
                    r5 = requests.get(f"{url_00}/{f_00}", stream=True, proxies=proxies)
                    r5.close()
                    r6 = requests.get(f"{url_01}/{f_01}", stream=True, proxies=proxies)
                    r6.close()
                    r7 = requests.get(f"{url_02}/{f_02}", stream=True, proxies=proxies)
                    r7.close()
                    r8 = requests.get(f"{url_03}/{f_03}", stream=True, proxies=proxies)
                    r8.close()
                    r9 = requests.get(f"{url_04}/{f_04}", stream=True, proxies=proxies)
                    r9.close()
                    break
                except Exception as e:
                    i = i  
                    
                    
    url_0 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{h_00.strftime('%Y%m%d')}&file={f_00}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_1 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{h_01.strftime('%Y%m%d')}&file={f_01}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_2 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{h_02.strftime('%Y%m%d')}&file={f_02}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_3 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{h_03.strftime('%Y%m%d')}&file={f_03}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_4 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{h_04.strftime('%Y%m%d')}&file={f_04}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")   
    
    
    url_5 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{d0.strftime('%Y%m%d')}&file={f_05}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_6 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{d1.strftime('%Y%m%d')}&file={f_06}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_7 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{d2.strftime('%Y%m%d')}&file={f_07}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_8 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{d3.strftime('%Y%m%d')}&file={f_08}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_9 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{d4.strftime('%Y%m%d')}&file={f_09}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")   
    
    urls = [
        url_0,
        url_1,
        url_2,
        url_3,
        url_4
    ]
    
    urls_dt = [
        
        url_5,
        url_6,
        url_7,
        url_8,
        url_9
        
    ]
    
    responses = [
        r0,
        r1,
        r2,
        r3,
        r4
    ]
    
    responses_dt = [
        r5,
        r6,
        r7,
        r8,
        r9
    ]
    
    for response, url, response_dt, url_dt in zip(responses, urls, responses_dt, urls_dt):
        if response.status_code == 200 and response_dt.status_code == 200:
            url = url
            url_dt = url_dt
            run = get_run_by_keyword(url)
            break        
    
    try:
        url = url
    except Exception as e:
        print(f"Latest analysis data is over 4 hours old. Aborting.....")
        sys.exit(1)
        
    parsed_url = urlparse(url)

    # Extract the query string
    query_string = parsed_url.query

    # Parse the query string into a dictionary of parameters
    query_params = parse_qs(query_string)

    # Access individual parameters
    filename = query_params.get('file', [''])[0] 
    
    parsed_url_dt = urlparse(url_dt)

    # Extract the query string
    query_string_dt = parsed_url_dt.query

    # Parse the query string into a dictionary of parameters
    query_params_dt = parse_qs(query_string_dt)

    # Access individual parameters
    filename_dt = query_params_dt.get('file', [''])[0] 
    
    filename_dt = f"{filename_dt}_dt"
    
    return url, url_dt, filename, filename_dt, run