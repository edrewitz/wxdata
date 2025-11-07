"""
This file hosts the NBM URL Scanner Functions.

These functions return the URL and filename for the latest available data on the dataservers.

(C) Eric J. Drewitz 2025
"""

import requests
import os
import numpy as np

from bs4 import BeautifulSoup
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

times = []
for h in range(0, 5, 1):
    date = now - timedelta(hours=h)
    times.append(date)
    
urls = []
for t in times:
    url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/blend/prod/blend.{t.strftime('%Y%m%d')}/{t.strftime('%H')}/core/"
    urls.append(url)

def nbm_url_scanner(proxies, 
                    region):
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The NBM
    goes out to 264 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    264 by the nereast increment of 1 hour in the first 36 hours and 3 hours for forecast times after 36 hours. 
    
    2) western_bound (Float or Integer) - The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - The northern bound of the data needed.

    5) southern_bound (Float or Integer) - The southern bound of the data needed.

    6) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
                        
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 
    
    8) variables (List) - A list of variable names the user wants to download in plain language. 
    
    """
    region = region.lower()
    
    if region != 'ak' and region != 'pr' and region != 'hi' and region != 'gu':
        region = 'co'
    else:
        region = region
    
    for url in urls:    
        if proxies==None:  
            response = requests.get(url, stream=True)
        else:
            response = requests.get(url, stream=True, proxies=proxies)
        if response.status_code == 200:
            html_content = response.text
            url = url
            run = int(f"{url[-8]}{url[-7]}")
            break
        else:
            pass                
                             
    soup = BeautifulSoup(html_content, 'html.parser')
    
    file_names = set() 

    for link in soup.find_all('a', href=True):
        href = link['href']
        if '.' in href and not href.startswith('#') and not href.startswith('mailto:'):
            filename = os.path.basename(href)
            file_names.add(filename)
            
    marker = ".idx"
    fnames = []
    for filename in sorted(list(file_names)):
        if marker not in filename:
            fnames.append(filename)
    
    files = []
    key = f".{region}.grib2"    
    for f in fnames:
        if key in f:
            files.append(f)
            
    return url, files, run