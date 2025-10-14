"""
This file hosts all the URL Scanner Functions.

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
    
    western_bound = convert_lon(western_bound)
    eastern_bound = convert_lon(eastern_bound)
    
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
    
    return url, filename

def rtma_comparison_url_scanner(model, 
                    cat,
                    western_bound, 
                    eastern_bound, 
                    northern_bound, 
                    southern_bound, 
                    proxies):
    
    """
    This function scans for the latest available RTMA Dataset within the past 4 hours and the dataset from 24 hours prior to the latest available dataset. 
    
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
    
    The URL path to the file and the filename for the most recent RTMA Dataset and the dataset for 24-hours prior to the latest available dataset.
    
    """
    model = model.upper()
    cat = cat.upper()
    
    western_bound = convert_lon(western_bound)
    eastern_bound = convert_lon(eastern_bound)
    
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
    
    d0 = h_00 - timedelta(hours=24)
    d1 = h_01 - timedelta(hours=24)
    d2 = h_02 - timedelta(hours=24)
    d3 = h_03 - timedelta(hours=24)
    d4 = h_04 - timedelta(hours=24)
            
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
        r0 = requests.get(f"{url_00}/{f_00}", stream=True)
        r1 = requests.get(f"{url_01}/{f_01}", stream=True)
        r2 = requests.get(f"{url_02}/{f_02}", stream=True)
        r3 = requests.get(f"{url_03}/{f_03}", stream=True)
        r4 = requests.get(f"{url_04}/{f_04}", stream=True)
        
        r5 = requests.get(f"{url_05}/{f_00}", stream=True)
        r6 = requests.get(f"{url_06}/{f_01}", stream=True)
        r7 = requests.get(f"{url_07}/{f_02}", stream=True)
        r8 = requests.get(f"{url_08}/{f_03}", stream=True)
        r9 = requests.get(f"{url_09}/{f_04}", stream=True)
        
    else:
        r0 = requests.get(f"{url_00}/{f_00}", stream=True, proxies=proxies)
        r1 = requests.get(f"{url_01}/{f_01}", stream=True, proxies=proxies)
        r2 = requests.get(f"{url_02}/{f_02}", stream=True, proxies=proxies)
        r3 = requests.get(f"{url_03}/{f_03}", stream=True, proxies=proxies)
        r4 = requests.get(f"{url_04}/{f_04}", stream=True, proxies=proxies)
        
        r5 = requests.get(f"{url_05}/{f_00}", stream=True, proxies=proxies)
        r6 = requests.get(f"{url_06}/{f_01}", stream=True, proxies=proxies)
        r7 = requests.get(f"{url_07}/{f_02}", stream=True, proxies=proxies)
        r8 = requests.get(f"{url_08}/{f_03}", stream=True, proxies=proxies)
        r9 = requests.get(f"{url_09}/{f_04}", stream=True, proxies=proxies)
        
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
             f"dir=%2F{directory}.{d0.strftime('%Y%m%d')}&file={f_00}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_6 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{d1.strftime('%Y%m%d')}&file={f_01}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_7 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{d2.strftime('%Y%m%d')}&file={f_02}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_8 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{d3.strftime('%Y%m%d')}&file={f_03}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    
    url_9 = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{directory}.pl?"
             f"dir=%2F{directory}.{d4.strftime('%Y%m%d')}&file={f_04}&all_var=on&all_lev=on&subregion=&"
             f"toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")   
    
    urls = [
        url_0,
        url_1,
        url_2,
        url_3,
        url_4
    ]
    
    urls_24 = [
        
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
    
    responses_24 = [
        r5,
        r6,
        r7,
        r8,
        r9
    ]
    
    for response, url, response_24, url_24 in zip(responses, urls, responses_24, urls_24):
        if response.status_code == 200 and response_24.status_code == 200:
            url = url
            url_24 = url_24
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
    
    parsed_url_24 = urlparse(url_24)

    # Extract the query string
    query_string_24 = parsed_url_24.query

    # Parse the query string into a dictionary of parameters
    query_params_24 = parse_qs(query_string_24)

    # Access individual parameters
    filename_24 = query_params_24.get('file', [''])[0] 
    
    filename_24 = f"{filename_24}_24"
    
    return url, url_24, filename, filename_24