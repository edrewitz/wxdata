    ##### IMPORTS NEEDED PYTHON MODULES #######
import xarray as xr
import urllib.request
import os
import sys
import logging
import glob
import warnings
warnings.filterwarnings('ignore')

from wxdata.scanner import file_scanner, url_scanner
from wxdata.utils import shift_longitude, lon_bounds, ens_folders
try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta

try:
    utc_time = datetime.now(UTC)
except Exception as e:
    utc_time = datetime.utcnow()

local_time = datetime.now()

yesterday = utc_time - timedelta(hours=24)


def gefs_0p25(cat, typeOfLevel, u_and_v_wind=False, western_bound=-180, eastern_bound=180, northern_bound=90, southern_bound=-90, proxies=None):

    """
    This function retrives the latest GEFS0p25 data. If the data is not previously downloaded nor up to date, the function
    will download and pre-process the latest dataset. 

    To avoid bans from the data servers, the function will scan the data server and locally hosted files and if the 
    files are up to date, the function will skip downloading the newest dataset. 

    Required Arguments:

    1) cat (String) - The category of the data. (i.e. mean, control, all members)

    2) typeOfLevel (String) - This determines which parameters are available for the GEFS 0.25x0.25 Ensemble Mean. The choices are as
       follows: 

      1) surface
      2) meanSea
      3) depthBelowLandLayer
      4) heightAboveGround
      5) atmosphereSingleLayer
      6) cloudCeiling
      7) heightAboveGroundLayer
      8) pressureFromGroundLayer

    Optional Arguments:
    
    1) u_and_v_wind (Boolean) - Default = False. When set to True, the function will return 2 datasets. 
       The first dataset being the u-component of the wind and second dataset the v-component of the wind. 
       When set to False, only 1 dataset is returned. 

    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    6) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }

    Returns
    -------

    An xarray.data array of the latest GEFS0p25 data for the bounds specified. 
    Files downloaded and pre-processed.                          
    """  
    sys.tracebacklimit = 0
    logging.disable()
    cat = cat.upper()
    model = 'GEFS0P25'

    if cat == 'MEAN' or cat == 'CONTROL':
        url, run = url_scanner(f"{model}", f"{cat}", proxies)
        download = file_scanner(f"{model}", f"{cat}", url, run)
        if cat == 'MEAN':
            ff = 'avg'
        if cat == 'CONTROL':
            ff = 'c00'
        western_bound, eastern_bound = lon_bounds(western_bound, eastern_bound)
        if download == True:
            print(f"Downloading the latest {model} data...")
    
            for file in os.listdir(f"{model}/{cat}"):
                try:
                    os.remove(f"{model}/{cat}/{file}")
                except Exception as e:
                    pass
            
            for i in range(0, 102, 3):
                if i < 10:
                    urllib.request.urlretrieve(f"{url}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f00{i}")
                    os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"{model}/{cat}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}")
                else:
                    urllib.request.urlretrieve(f"{url}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f0{i}")
                    os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"{model}/{cat}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}")
            for i in range(102, 243, 3):
                urllib.request.urlretrieve(f"{url}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f{i}")
                os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"{model}/{cat}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}")  

            for i in range(0, 102, 3):
                if i < 10:
                    try:
                        os.replace(f"{model}/{cat}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"{model}/{cat}/ge{ff}.t{run}z.pgrb2s.0p25_f00{i}.grib2")
                    except Exception as e:
                        pass
                else:
                    try:
                        os.replace(f"{model}/{cat}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"{model}/{cat}/ge{ff}.t{run}z.pgrb2s.0p25_f0{i}.grib2")
                    except Exception as e:
                        pass
            
            for i in range(102, 243, 3):
                try:
                    os.replace(f"{model}/{cat}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"{model}/{cat}/ge{ff}.t{run}z.pgrb2s.0p25_f{i}.grib2")
                except Exception as e:
                    pass        

        else:
            print(f"Data in f:{model}/{cat} is current. Skipping download.")
            
        file_pattern = f"{model}/{cat}/*.grib2"
        
        if u_and_v_wind == True:
            u = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName': '10u'}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
            v = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName': '10v'}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            u = shift_longitude(u)
            v = shift_longitude(v)

            for item in os.listdir(f"{model}/{cat}"):
                if item.endswith(".idx"):
                    os.remove(f"{model}/{cat}/{item}")

            return u, v

        else:
            ds = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': typeOfLevel}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            ds = shift_longitude(ds)

            for item in os.listdir(f"{model}/{cat}"):
                if item.endswith(".idx"):
                    os.remove(f"{model}/{cat}/{item}")

            return ds

    else:
        paths = ens_folders(model, cat, 30)
        url, run = url_scanner(f"{model}", f"{cat}", proxies)
        download = file_scanner(f"{model}", f"{cat}", url, run, ens_members=True)
        western_bound, eastern_bound = lon_bounds(western_bound, eastern_bound)

        if download == True:
            print(f"Downloading the latest {model} data...")
            for pp in range(0, 30, 1):
                for file in os.listdir(f"{paths[pp]}"):
                    try:
                        os.remove(f"{paths[pp]}/{file}")
                    except Exception as e:
                        pass            

            for e, p in zip(range(1, 31, 1), range(0, 30, 1)):
                if e < 10:
                    ff = f"p0{e}"
                else:
                    ff = f"p{e}"
                        
                for i in range(0, 102, 3):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f00{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"{paths[p]}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}")
                    else:
                        urllib.request.urlretrieve(f"{url}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f0{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"{paths[p]}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}")
                for i in range(102, 243, 3):
                    urllib.request.urlretrieve(f"{url}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f{i}")
                    os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"{paths[p]}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}")  
                            
                for i in range(0, 102, 3):
                    if i < 10:
                        try:
                            os.replace(f"{paths[p]}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"{paths[p]}/ge{ff}.t{run}z.pgrb2s.0p25_f00{i}.grib2")
                        except Exception as e:
                            pass
                    else:
                        try:
                            os.replace(f"{paths[p]}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"{paths[p]}/ge{ff}.t{run}z.pgrb2s.0p25_f0{i}.grib2")
                        except Exception as e:
                            pass
                
                for i in range(102, 243, 3):
                    try:
                        os.replace(f"{paths[p]}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"{paths[p]}/ge{ff}.t{run}z.pgrb2s.0p25_f{i}.grib2")
                    except Exception as e:
                        pass    

        else:
            print(f"Data in f:{model}/{cat} is current. Skipping download.")

        ds_list = []
        u_list = []
        v_list = []

        for p in range(0, 30, 1):
            file_pattern = f"{paths[p]}/*.grib2"
    
            if u_and_v_wind == True:
                u = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName': '10u'}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                v = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName': '10v'}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
    
                u = shift_longitude(u)
                v = shift_longitude(v)
                u_list.append(u)
                v_list.append(v)

                for item in os.listdir(f"{paths[p]}"):
                    if item.endswith(".idx"):
                        os.remove(f"{paths[p]}/{item}")
    
    
            else:
                    ds = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': typeOfLevel}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
        
                    ds = shift_longitude(ds)
                    ds_list.append(ds)
    
                    for item in os.listdir(f"{paths[p]}"):
                        if item.endswith(".idx"):
                            os.remove(f"{paths[p]}/{item}")

        if u_and_v_wind == True:
            u = xr.concat(u_list, dim='number')
            v = xr.concat(v_list, dim='number')
            return u, v
        else:
            ds = xr.concat(ds_list, dim='number')
            return ds
