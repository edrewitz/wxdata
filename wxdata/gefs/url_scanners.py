"""
This file hosts the GEFS URL Scanner Functions.

These functions return the URL and filename for the latest available data on the dataservers.

(C) Eric J. Drewitz 2025
"""

import requests
import sys
import numpy as np

from urllib.parse import urlparse, parse_qs
from wxdata.utils.coords import convert_lon
from wxdata.gefs.exception_messages import(
    
    gefs0p50,
    gefs0p25
)

from wxdata.utils.nomads_gribfilter import(
    
    result_string,
    key_list
)

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

def gefs_0p50_url_scanner(cat, 
                          final_forecast_hour, 
                          western_bound, 
                          eastern_bound, 
                          northern_bound, 
                          southern_bound, 
                          proxies, 
                          step, 
                          members,
                          variables):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - The northern bound of the data needed.

    6) southern_bound (Float or Integer) - The southern bound of the data needed.

    7) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
                        
    8) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 
    
    9) members (List) The individual ensemble members. There are 30 members in this ensemble.  
    
    10) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50
        -------------------------------
        
			'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'categorical rain'
            'categorical snow'
            'convective inhibition'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'geopotential height'
            'ice thickness'
            'latent heat net flux'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'sensible heat net flux'
            'snow depth'
            'volumetric soil moisture content'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'soil temperature'
            'u-component of wind'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'v-component of wind'
            'vertical velocity'
            'water equivalent of accumulated snow depth'
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, download URL and server response code.     
    """
    # Makes the category all lower case for consistency
    cat = cat.lower()
    
    # Converts the longitude from -180 to 180 into 0 to 360
    western_bound, eastern_bound = convert_lon(western_bound, eastern_bound)
    
    m = []
    for member in members:
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"      
        
        m.append(aa) 
    
    # Gets the file abbreviation based on category
    # Ensemble Mean
    if cat == 'mean':
        aa = f"avg"
    # Ensemble Members
    elif cat == 'members':
        member = members[-1]
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"
    # Control Run
    elif cat == 'control':
        aa = f"c00"
    # Ensemble Spread
    elif cat == 'spread':
        aa = f"spr"
    # User enters an invalid category
    # When a category is invalid - Defaults to Ensemble Mean
    else:
        gefs0p50.gefs0p50_cat_error('gefs0p50')
        aa = f"avg"
        
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 384:
        gefs0p50.forecast_hour_error()
        final_forecast_hour = 384
    else:
        final_forecast_hour = final_forecast_hour
        
    if final_forecast_hour >= 100:
        final_forecast_hour = f"{final_forecast_hour}"
    elif final_forecast_hour >= 10 and final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = f"00{final_forecast_hour}"
           
    # These are the different download URLs for the various runtimes in the past 24 hours
    
    # URLs to scan for the latest file
    today_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/18/atmos/pgrb2ap5/")
    today_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/12/atmos/pgrb2ap5/")
    today_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/06/atmos/pgrb2ap5/")
    today_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/00/atmos/pgrb2ap5/")
    
    yesterday_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/18/atmos/pgrb2ap5/")
    yesterday_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/12/atmos/pgrb2ap5/")
    yesterday_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/06/atmos/pgrb2ap5/")
    yesterday_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/00/atmos/pgrb2ap5/")
    
    # Gets the variable list in a string format convered to GRIB filter keys
    
    keys = key_list(variables)
    params = result_string(keys)
        
    # Today's runs
    today_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    # Yesterday's runs
    yd_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    

    # The filenames for the different run times
    f_18z = f"ge{aa}.t18z.pgrb2a.0p50.f{final_forecast_hour}"
    f_12z = f"ge{aa}.t12z.pgrb2a.0p50.f{final_forecast_hour}"
    f_06z = f"ge{aa}.t06z.pgrb2a.0p50.f{final_forecast_hour}"
    f_00z = f"ge{aa}.t00z.pgrb2a.0p50.f{final_forecast_hour}"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)   
                    break
                except Exception as e:
                    i = i     
    
    
    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    break
                except Exception as e:
                    i = i
        
    # Creates a list of URLs and URL responses to loop through when checking
    
    urls = [
        today_18z,
        today_12z,
        today_06z,
        today_00z,
        yd_18z,
        yd_12z,
        yd_06z,
        yd_18z
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
            run = int(f"{url[121]}{url[122]}")
            break        
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
    
    if step == 6:
        if int(final_forecast_hour) > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = int(final_forecast_hour) + step
    elif step == 3:
        if int(final_forecast_hour) > 100:
            step = 3
            stop = 99 + step
            start = 102
        else:
            step = 3
            stop = int(final_forecast_hour) + step
    else:
        print("ERROR! User entered an invalid step value\nDefaulting to 6 hourly.")
        if int(final_forecast_hour) > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = int(final_forecast_hour) + step
        
        
    urls = []
    
    if cat != 'members':
    
        if url == today_18z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == today_12z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == today_06z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == today_00z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == yd_18z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == yd_12z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == yd_06z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        else:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
        
    else:
        if url == today_18z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)  
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == today_12z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == today_06z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == today_00z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == yd_18z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t18z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == yd_12z:
                for i in range(0, stop, step):
                    for aa in m:
                        if i < 10:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f00{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        else:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f0{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                            
                        urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        for aa in m:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                    f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f{i}{params}&"
                                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                            
                            urls.append(url)
                            
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        for aa in m:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                    f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t12z.pgrb2a.0p50.f{i}{params}&"
                                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                            
                            urls.append(url)
                        
        elif url == yd_06z:
            for aa in m:
                for i in range(0, stop, step):
                        if i < 10:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f00{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        else:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f0{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                            
                        urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t06z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        else:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2ap5&file=ge{aa}.t00z.pgrb2a.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
        
    # Extract the filename
    # Parse the URL
    filenames = []
    for url in urls:
        
        parsed_url = urlparse(url)

        # Extract the query string
        query_string = parsed_url.query

        # Parse the query string into a dictionary of parameters
        query_params = parse_qs(query_string)

        # Access individual parameters
        filename = query_params.get('file', [''])[0] 
        
        filenames.append(filename)
        
    
    return urls, filenames, run


def gefs_0p50_secondary_parameters_url_scanner(cat, 
                          final_forecast_hour, 
                          western_bound, 
                          eastern_bound, 
                          northern_bound, 
                          southern_bound, 
                          proxies, 
                          step, 
                          members,
                          variables):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) control
    4) spread
    
    
    2) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P50 SECONDARY PARAMETERS
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - The northern bound of the data needed.

    6) southern_bound (Float or Integer) - The southern bound of the data needed.

    7) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
                        
    8) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 
    
    9) members (List) The individual ensemble members. There are 30 members in this ensemble.  
    
    10) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50 SECONDARY PARAMETERS
        ----------------------------------------------------
        
        'best lifted index'
        '5 wave geopotential height'
        'absolute vorticity'
        'temperature'
        'dew point'
        'convective precipitation'
        'albedo'
        'apparent temperature'
        'brightness temperature'
        'convective available potential energy'
        'clear sky uv-b downward solar flux'
        'convective inhibition'
        'cloud mixing ratio'
        'plant canopy surface water'
        'percent frozen precipitaion'
        'convective precipitation rate'
        'cloud water'
        'cloud work function'
        'uv-b downward solar flux'
        'field capacity'
        'surface friction velocity'
        'ground heat flux'
        'wind gust'
        'geopotential height'
        'haines index'
        'storm relative helicity'
        'planetary boundary layer height'
        'icao standard atmosphere reference height'
        'ice cover'
        'icing'
        'icing severity'
        'land cover'
        'surface lifted index'
        'montgomery stream function'
        'mslp (eta model reduction)'
        'large scale non-convective precipitation'
        'ozone mixing ratio'
        'potential evaporation rate'
        'parcel lifted index (to 500mb)'
        'pressure level from which parcel was lifted'
        'potential temperature'
        'precipitation rate'
        'pressure'
        'potential vorticity'
        'precipitable water'
        'relative humidity'
        'surface roughness'
        'snow phase-change heat flux'
        'snow cover'
        'liquid volumetric soil moisture (non-frozen)'
        'volumetric soil moisture content'
        'specific humidity'
        'sunshine duration'
        'total cloud cover'
        'total ozone'
        'soil temperature'
        'momentum flux (u-component)'
        'u-component of wind'
        'zonal flux of gravity wave stress'
        'u-component of storm motion'
        'upward shortwave radiation flux'
        'momentum flux (v-component)'
        'v-component of wind'
        'meridional flux of gravity wave stress'
        'visibility'
        'ventilation rate'
        'v-component of storm motion'
        'vertical velocity'
        'vertical speed shear'
        'water runoff'
        'wilting point'
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, download URL and server response code.        
    """
    # Makes the category all lower case for consistency
    cat = cat.lower()
    
    # Converts the longitude from -180 to 180 into 0 to 360
    western_bound, eastern_bound = convert_lon(western_bound, eastern_bound)
    
    m = []
    for member in members:
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"      
        
        m.append(aa) 
    
    # Gets the file abbreviation based on category
    # Ensemble Mean
    if cat == 'members' or cat == 'mean' or cat == 'spread':
        member = members[-1]
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"
    # Control Run
    elif cat == 'control':
        aa = f"c00"
    # User enters an invalid category
    # When a category is invalid - Defaults to Control Run
    else:
        gefs0p50.gefs0p50_cat_error('gefs0p50 secondary parameters')
        aa = f"c00"
        
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 384:
        gefs0p50.forecast_hour_error()
        final_forecast_hour = 384
    else:
        final_forecast_hour = final_forecast_hour
        
    if final_forecast_hour >= 100:
        final_forecast_hour = f"{final_forecast_hour}"
    elif final_forecast_hour >= 10 and final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = f"00{final_forecast_hour}"
           
    # These are the different download URLs for the various runtimes in the past 24 hours
    
    # URLs to scan for the latest file
    
    today_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/18/atmos/pgrb2bp5/")
    today_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/12/atmos/pgrb2bp5/")
    today_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/06/atmos/pgrb2bp5/")
    today_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/00/atmos/pgrb2bp5/")
    
    yesterday_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/18/atmos/pgrb2bp5/")
    yesterday_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/12/atmos/pgrb2bp5/")
    yesterday_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/06/atmos/pgrb2bp5/")
    yesterday_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/00/atmos/pgrb2bp5/")
        
    # Gets the variable list in a string format convered to GRIB filter keys
    
    keys = key_list(variables)
    params = result_string(keys)        

    # Today's runs
    today_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    # Yesterday's runs
    yd_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    

    # The filenames for the different run times
    f_18z = f"ge{aa}.t18z.pgrb2b.0p50.f{final_forecast_hour}"
    f_12z = f"ge{aa}.t12z.pgrb2b.0p50.f{final_forecast_hour}"
    f_06z = f"ge{aa}.t06z.pgrb2b.0p50.f{final_forecast_hour}"
    f_00z = f"ge{aa}.t00z.pgrb2b.0p50.f{final_forecast_hour}"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)  
                    break
                except Exception as e:
                    i = i                  
        
    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)   
                    break
                except Exception as e:
                    i = i                 
        
    # Creates a list of URLs and URL responses to loop through when checking
    
    urls = [
        today_18z,
        today_12z,
        today_06z,
        today_00z,
        yd_18z,
        yd_12z,
        yd_06z,
        yd_18z
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
            run = int(f"{url[121]}{url[122]}")
            break      
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
    
    if step == 6:
        if int(final_forecast_hour) > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = int(final_forecast_hour) + step
    elif step == 3:
        if int(final_forecast_hour) > 100:
            step = 3
            stop = 99 + step
            start = 102
        else:
            step = 3
            stop = int(final_forecast_hour) + step
    else:
        print("ERROR! User entered an invalid step value\nDefaulting to 6 hourly.")
        if int(final_forecast_hour) > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = int(final_forecast_hour) + step
        
        
    urls = []
    
    if cat != 'members' and cat != 'mean' and cat != 'spread':
    
        if url == today_18z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == today_12z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == today_06z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == today_00z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == yd_18z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == yd_12z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == yd_06z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        else:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 240:
                for i in range(start, int(final_forecast_hour) + 6, 6):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
        
    else:
        if url == today_18z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)  
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == today_12z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == today_06z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == today_00z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == yd_18z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t18z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == yd_12z:
                for i in range(0, stop, step):
                    for aa in m:
                        if i < 10:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f00{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        else:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f0{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                            
                        urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        for aa in m:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                    f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f{i}{params}&"
                                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                            
                            urls.append(url)
                            
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        for aa in m:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                    f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t12z.pgrb2b.0p50.f{i}{params}&"
                                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                            
                            urls.append(url)
                        
        elif url == yd_06z:
            for aa in m:
                for i in range(0, stop, step):
                        if i < 10:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f00{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        else:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f0{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                            
                        urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t06z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        else:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100 and int(final_forecast_hour) <= 240:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
                if int(final_forecast_hour) > 240:
                    for i in range(start, int(final_forecast_hour) + 6, 6):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50b.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2bp5&file=ge{aa}.t00z.pgrb2b.0p50.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
        
    # Extract the filename
    # Parse the URL
    filenames = []
    for url in urls:
        
        parsed_url = urlparse(url)

        # Extract the query string
        query_string = parsed_url.query

        # Parse the query string into a dictionary of parameters
        query_params = parse_qs(query_string)

        # Access individual parameters
        filename = query_params.get('file', [''])[0] 
        
        filenames.append(filename)
        
    
    return urls, filenames, run
            

def gefs_0p25_url_scanner(cat, 
                          final_forecast_hour, 
                          western_bound, 
                          eastern_bound, 
                          northern_bound, 
                          southern_bound, 
                          proxies, 
                          step, 
                          members,
                          variables):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P25
    goes out to 240 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    240 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - The northern bound of the data needed.

    6) southern_bound (Float or Integer) - The southern bound of the data needed.

    7) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
                        
    8) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 
    
    9) members (List) The individual ensemble members. There are 30 members in this ensemble.  
    
    10) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P25
        -------------------------------
        
			'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'categorical rain'
            'categorical snow'
            'convective inhibition'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'geopotential height'
            'ice thickness'
            'latent heat net flux'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'sensible heat net flux'
            'snow depth'
            'volumetric soil moisture content'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'soil temperature'
            'u-component of wind'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'v-component of wind'
            'vertical velocity'
            'water equivalent of accumulated snow depth'
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, download URL and server response code.    
    """
    # Makes the category all lower case for consistency
    cat = cat.lower()
    
    # Converts the longitude from -180 to 180 into 0 to 360
    western_bound, eastern_bound = convert_lon(western_bound, eastern_bound)
    
    m = []
    for member in members:
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"      
        
        m.append(aa) 
    
    # Gets the file abbreviation based on category
    # Ensemble Mean
    if cat == 'mean':
        aa = f"avg"
    # Ensemble Members
    elif cat == 'members':
        member = members[-1]
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"
    # Control Run
    elif cat == 'control':
        aa = f"c00"
    # Ensemble Spread
    elif cat == 'spread':
        aa = f"spr"
    # User enters an invalid category
    # When a category is invalid - Defaults to Ensemble Mean
    else:
        gefs0p25.gefs0p25_cat_error()
        aa = f"avg"
        
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 240:
        gefs0p25.forecast_hour_error()
        final_forecast_hour = 240
    else:
        final_forecast_hour = final_forecast_hour
        
    if final_forecast_hour >= 100:
        final_forecast_hour = f"{final_forecast_hour}"
    elif final_forecast_hour >= 10 and final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = f"00{final_forecast_hour}"
           
    # These are the different download URLs for the various runtimes in the past 24 hours
    
    # URLs to scan for the latest file
    today_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/18/atmos/pgrb2sp25/")
    today_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/12/atmos/pgrb2sp25/")
    today_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/06/atmos/pgrb2sp25/")
    today_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/00/atmos/pgrb2sp25/")
    
    yesterday_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/18/atmos/pgrb2sp25/")
    yesterday_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/12/atmos/pgrb2sp25/")
    yesterday_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/06/atmos/pgrb2sp25/")
    yesterday_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/00/atmos/pgrb2sp25/")
    
    # Gets the variable list in a string format convered to GRIB filter keys
    
    keys = key_list(variables)
    params = result_string(keys)
        
    # Today's runs
    today_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    # Yesterday's runs
    yd_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    

    # The filenames for the different run times
    f_18z = f"ge{aa}.t18z.pgrb2s.0p25.f{final_forecast_hour}"
    f_12z = f"ge{aa}.t12z.pgrb2s.0p25.f{final_forecast_hour}"
    f_06z = f"ge{aa}.t06z.pgrb2s.0p25.f{final_forecast_hour}"
    f_00z = f"ge{aa}.t00z.pgrb2s.0p25.f{final_forecast_hour}"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)   
                    break
                except Exception as e:
                    i = i                 
        
    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)  
                    break
                except Exception as e:
                    i = i                  
        
    # Creates a list of URLs and URL responses to loop through when checking
    
    urls = [
        today_18z,
        today_12z,
        today_06z,
        today_00z,
        yd_18z,
        yd_12z,
        yd_06z,
        yd_18z
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
            run = int(f"{url[122]}{url[123]}")
            break      
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
    
    if step == 6:
        if int(final_forecast_hour) > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = int(final_forecast_hour) + step
    elif step == 3:
        if int(final_forecast_hour) > 100:
            step = 3
            stop = 99 + step
            start = 102
        else:
            step = 3
            stop = int(final_forecast_hour) + step
    else:
        print("ERROR! User entered an invalid step value\nDefaulting to 6 hourly.")
        if int(final_forecast_hour) > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = int(final_forecast_hour) + step
        
        
    urls = []
    
    if cat != 'members':
    
        if url == today_18z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == today_12z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == today_06z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == today_00z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == yd_18z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                    
            if int(final_forecast_hour) > 100:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == yd_12z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        elif url == yd_06z:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
                        
        else:
            for i in range(0, stop, step):
                if i < 10:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f00{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                else:
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                        f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f0{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                urls.append(url)
                    
            if int(final_forecast_hour) > 100:
                for i in range(start, int(final_forecast_hour) + step, step):
                    url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    
                    urls.append(url)
        
    else:
        if url == today_18z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)  
                if int(final_forecast_hour) > 100:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == today_12z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == today_06z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == today_00z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                                f"?dir=%2Fgefs.{now.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == yd_18z:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t18z.pgrb2s.0p25.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        elif url == yd_12z:
                for i in range(0, stop, step):
                    for aa in m:
                        if i < 10:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f00{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        else:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f0{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                            
                        urls.append(url)
                    
                if int(final_forecast_hour) > 100:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        for aa in m:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                                    f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t12z.pgrb2s.0p25.f{i}{params}&"
                                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                            
                            urls.append(url)
                        
        elif url == yd_06z:
            for aa in m:
                for i in range(0, stop, step):
                        if i < 10:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f00{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        else:
                            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f0{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                            
                        urls.append(url)
                    
                if int(final_forecast_hour) > 100:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t06z.pgrb2s.0p25.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
                        
        else:
            for aa in m:
                for i in range(0, stop, step):
                    if i < 10:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f00{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                    else:
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                            f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f0{i}{params}&"
                            f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                    urls.append(url)
                    
                if int(final_forecast_hour) > 100:
                    for i in range(start, int(final_forecast_hour) + step, step):
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl"
                                f"?dir=%2Fgefs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos%2Fpgrb2sp25&file=ge{aa}.t00z.pgrb2s.0p25.f{i}{params}&"
                                f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                        
                        urls.append(url)
        
    # Extract the filename
    # Parse the URL
    filenames = []
    for url in urls:
        
        parsed_url = urlparse(url)

        # Extract the query string
        query_string = parsed_url.query

        # Parse the query string into a dictionary of parameters
        query_params = parse_qs(query_string)

        # Access individual parameters
        filename = query_params.get('file', [''])[0] 
        
        filenames.append(filename)
        
    
    return urls, filenames, run