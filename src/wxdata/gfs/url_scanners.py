"""
This file hosts the GFS URL Scanner Functions.

These functions return the URL and filename for the latest available data on the dataservers.

(C) Eric J. Drewitz 2025
"""

import requests
import sys
import numpy as np

from urllib.parse import urlparse, parse_qs
from wxdata.utils.coords import convert_lon

from wxdata.utils.nomads_gribfilter import(
    
    result_string,
    key_list
)

from wxdata.gfs.exception_messages import(
    
    forecast_hour_error,
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

def assign_cat(cat):
    
    """
    This function converts the category into the abbreviation used on the NCEP/NOMADS server.
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) atmosphere
    2) ocean
    
    Optional Arguments: None
    
    Returns
    -------    
    
    The abbreviation used on NOMADS (atmos or wave)
    """
    
    cats = {
        'atmosphere':'atmos',
        'ocean':'wave'
    }
    
    return cats[cat]

def gfs_0p50_url_scanner(final_forecast_hour, 
                          western_bound, 
                          eastern_bound, 
                          northern_bound, 
                          southern_bound, 
                          proxies, 
                          step, 
                          variables):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) atmosphere
    
    
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
    
    The model runtime and the download URL.     
    """
    # Makes the category all lower case for consistency
    
    # Converts the longitude from -180 to 180 into 0 to 360
    western_bound, eastern_bound = convert_lon(western_bound, eastern_bound)
    
        
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 384:
        forecast_hour_error()
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
    today_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/18/atmos/")
    today_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/12/atmos/")
    today_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/06/atmos/")
    today_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/00/atmos/")
    
    yesterday_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/18/atmos/")
    yesterday_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/12/atmos/")
    yesterday_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/06/atmos/")
    yesterday_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/00/atmos/")
    
    # Gets the variable list in a string format convered to GRIB filter keys
    
    keys = key_list(variables)
    params = result_string(keys)
        
    # Today's runs
    today_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    # Yesterday's runs
    yd_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    

    # The filenames for the different run times
    f_18z = f"gfs.t18z.pgrb2full.0p50.f{final_forecast_hour}"
    f_12z = f"gfs.t12z.pgrb2full.0p50.f{final_forecast_hour}"
    f_06z = f"gfs.t06z.pgrb2full.0p50.f{final_forecast_hour}"
    f_00z = f"gfs.t00z.pgrb2full.0p50.f{final_forecast_hour}"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)
            y_00.close()
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)
                    y_00.close()
                    break
                except Exception as e:
                    i = i       
                    

    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
            y_00.close()
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    y_00.close()
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
            run = int(f"{url[78]}{url[79]}")
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
    
    
    if url == today_18z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == today_12z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == today_06z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == today_00z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == yd_18z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == yd_12z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == yd_06z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    else:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f{i}{params}&"
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

def gfs_0p25_url_scanner(final_forecast_hour, 
                          western_bound, 
                          eastern_bound, 
                          northern_bound, 
                          southern_bound, 
                          proxies, 
                          step, 
                          variables):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) atmosphere
    2) ocean
    
    
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
    
    The model runtime and the download URL.     
    """
    
    # Converts the longitude from -180 to 180 into 0 to 360
    western_bound, eastern_bound = convert_lon(western_bound, eastern_bound)
    
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 384:
        forecast_hour_error()
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
    today_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/18/atmos/")
    today_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/12/atmos/")
    today_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/06/atmos/")
    today_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/00/atmos/")
    
    yesterday_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/18/atmos/")
    yesterday_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/12/atmos/")
    yesterday_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/06/atmos/")
    yesterday_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/00/atmos/")
    
    # Gets the variable list in a string format convered to GRIB filter keys
    
    keys = key_list(variables)
    params = result_string(keys)
        
    # Today's runs
    today_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    # Yesterday's runs
    yd_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    

    # The filenames for the different run times
    f_18z = f"gfs.t18z.pgrb2.0p25.f{final_forecast_hour}"
    f_12z = f"gfs.t12z.pgrb2.0p25.f{final_forecast_hour}"
    f_06z = f"gfs.t06z.pgrb2.0p25.f{final_forecast_hour}"
    f_00z = f"gfs.t00z.pgrb2.0p25.f{final_forecast_hour}"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)
            y_00.close()
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)
                    y_00.close()
                    break
                except Exception as e:
                    i = i       
                    

    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
            y_00.close()
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    y_00.close()
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
            run = int(f"{url[78]}{url[79]}")
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
    
    
    if url == today_18z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == today_12z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == today_06z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == today_00z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == yd_18z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == yd_12z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == yd_06z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    else:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2.0p25.f{i}{params}&"
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


def gfs_0p25_secondary_parameters_url_scanner(final_forecast_hour, 
                          western_bound, 
                          eastern_bound, 
                          northern_bound, 
                          southern_bound, 
                          proxies, 
                          step, 
                          variables):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) atmosphere
    2) ocean
    
    
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
    
    The model runtime and the download URL.     
    """
    
    # Converts the longitude from -180 to 180 into 0 to 360
    western_bound, eastern_bound = convert_lon(western_bound, eastern_bound)
        
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 384:
        forecast_hour_error()
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
    today_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/18/atmos/")
    today_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/12/atmos/")
    today_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/06/atmos/")
    today_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/00/atmos/")
    
    yesterday_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/18/atmos/")
    yesterday_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/12/atmos/")
    yesterday_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/06/atmos/")
    yesterday_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/00/atmos/")
    
    # Gets the variable list in a string format convered to GRIB filter keys
    
    keys = key_list(variables)
    params = result_string(keys)
        
    # Today's runs
    today_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2b.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2b.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2b.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2b.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    # Yesterday's runs
    yd_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2b.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2b.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2b.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2b.0p25.f{final_forecast_hour}{params}&"
        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    

    # The filenames for the different run times
    f_18z = f"gfs.t18z.pgrb2b.0p25.f{final_forecast_hour}"
    f_12z = f"gfs.t12z.pgrb2b.0p25.f{final_forecast_hour}"
    f_06z = f"gfs.t06z.pgrb2b.0p25.f{final_forecast_hour}"
    f_00z = f"gfs.t00z.pgrb2b.0p25.f{final_forecast_hour}"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)
            y_00.close()
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)
                    y_00.close()
                    break
                except Exception as e:
                    i = i       
                    

    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
            y_00.close()
        except Exception as e:
            for i in range(0, 5, 1):
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    y_00.close()
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
            run = int(f"{url[79]}{url[80]}")
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
    
    
    if url == today_18z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2b.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2b.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2b.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == today_12z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2b.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2b.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2b.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == today_06z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2b.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2b.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2b.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == today_00z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2b.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2b.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2b.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == yd_18z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2b.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2b.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2b.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == yd_12z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2b.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2b.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2b.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == yd_06z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2b.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2b.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2b.0p25.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    else:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2b.0p25.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2b.0p25.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2b.0p25.f{i}{params}&"
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
