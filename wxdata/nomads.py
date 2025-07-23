##### IMPORTS NEEDED PYTHON MODULES #######
import xarray as xr
import urllib.request
import os
import sys
import logging
import time
import glob
import warnings
#warnings.filterwarnings('ignore')

from scanner import scanner
from utils import shift_longitude, lon_bounds
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


def gefs_0p25(data, typeOfLevel, u_and_v_wind=False, western_bound=-180, eastern_bound=180, northern_bound=90, southern_bound=-90, proxies=None):

    """
                         
    """  
    sys.tracebacklimit = 0
    logging.disable()

    if data == 'Mean' or data == 'mean' or data == 'MEAN':
        url = scanner('GEFS0p25 Ensemble Mean', proxies)
        run = f"{url[-19]}{url[-18]}"
        model = 'GEFS0p25 Mean'
        western_bound, eastern_bound = lon_bounds(western_bound, eastern_bound)

        if os.path.exists(f"{model}"):
            if os.path.exists(f"{model}/geavg.t{run}z.pgrb2s.0p25_f240.grib2"):
                modification_timestamp = os.path.getmtime(f"{model}/geavg.t{run}z.pgrb2s.0p25_f240.grib2")
                readable_time = time.ctime(modification_timestamp)
                update_day = int(f"{readable_time[8]}{readable_time[8]}")
                update_hour = int(f"{readable_time[11]}{readable_time[12]}")
                diff = local_time.hour - update_hour
                if update_day != local_time.day:
                    print(f"Data in {model} folder is old. Downloading Latest Data...")
    
                    for file in os.listdir(f"{model}"):
                        try:
                            os.remove(f"{model}/{file}")
                        except Exception as e:
                            pass
                    
                    for i in range(0, 102, 3):
                        if i < 10:
                            urllib.request.urlretrieve(f"{url}/geavg.t{run}z.pgrb2s.0p25.f00{i}", f"geavg.t{run}z.pgrb2s.0p25.f00{i}")
                            os.replace(f"geavg.t{run}z.pgrb2s.0p25.f00{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25.f00{i}")
                        else:
                            urllib.request.urlretrieve(f"{url}/geavg.t{run}z.pgrb2s.0p25.f0{i}", f"geavg.t{run}z.pgrb2s.0p25.f0{i}")
                            os.replace(f"geavg.t{run}z.pgrb2s.0p25.f0{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25.f0{i}")
                    for i in range(102, 243, 3):
                        urllib.request.urlretrieve(f"{url}/geavg.t{run}z.pgrb2s.0p25.f{i}", f"geavg.t{run}z.pgrb2s.0p25.f{i}")
                        os.replace(f"geavg.t{run}z.pgrb2s.0p25.f{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25.f{i}")  

                    for i in range(0, 102, 3):
                        if i < 10:
                            try:
                                os.replace(f"{model}/geavg.t{run}z.pgrb2s.0p25.f00{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25_f00{i}.grib2")
                            except Exception as e:
                                pass
                        else:
                            try:
                                os.replace(f"{model}/geavg.t{run}z.pgrb2s.0p25.f0{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25_f0{i}.grib2")
                            except Exception as e:
                                pass
                    
                    for i in range(102, 243, 3):
                        try:
                            os.replace(f"{model}/geavg.t{run}z.pgrb2s.0p25.f{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25_f{i}.grib2")
                        except Exception as e:
                            pass        

                if update_day == local_time.day and diff > 6:
                    print(f"Data in {model} folder is old. Downloading Latest Data...")
    
                    for file in os.listdir(f"{model}"):
                        try:
                            os.remove(f"{model}/{file}")
                        except Exception as e:
                            pass
                    
                    for i in range(0, 102, 3):
                        if i < 10:
                            urllib.request.urlretrieve(f"{url}/geavg.t{run}z.pgrb2s.0p25.f00{i}", f"geavg.t{run}z.pgrb2s.0p25.f00{i}")
                            os.replace(f"geavg.t{run}z.pgrb2s.0p25.f00{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25.f00{i}")
                        else:
                            urllib.request.urlretrieve(f"{url}/geavg.t{run}z.pgrb2s.0p25.f0{i}", f"geavg.t{run}z.pgrb2s.0p25.f0{i}")
                            os.replace(f"geavg.t{run}z.pgrb2s.0p25.f0{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25.f0{i}")
                    for i in range(102, 243, 3):
                        urllib.request.urlretrieve(f"{url}/geavg.t{run}z.pgrb2s.0p25.f{i}", f"geavg.t{run}z.pgrb2s.0p25.f{i}")
                        os.replace(f"geavg.t{run}z.pgrb2s.0p25.f{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25.f{i}") 

                    for i in range(0, 102, 3):
                        if i < 10:
                            try:
                                os.replace(f"{model}/geavg.t{run}z.pgrb2s.0p25.f00{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25_f00{i}.grib2")
                            except Exception as e:
                                pass
                        else:
                            try:
                                os.replace(f"{model}/geavg.t{run}z.pgrb2s.0p25.f0{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25_f0{i}.grib2")
                            except Exception as e:
                                pass
                    
                    for i in range(102, 243, 3):
                        try:
                            os.replace(f"{model}/geavg.t{run}z.pgrb2s.0p25.f{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25_f{i}.grib2")
                        except Exception as e:
                            pass        

                else:
                    print(f"Already Satisfied: Latest {model} Data In Folder.")
                file_pattern = f"{model}/*.grib2"
        
                if u_and_v_wind == True:
                    u = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName': '10u'}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                    v = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName': '10v'}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
        
                    u = shift_longitude(u)
                    v = shift_longitude(v)
        
                    for item in os.listdir(f"{model}"):
                        if item.endswith(".idx"):
                            os.remove(f"{model}/{item}")
        
                    return u, v
        
                else:
                    ds = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': typeOfLevel}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
        
                    ds = shift_longitude(ds)


        
                    for item in os.listdir(f"{model}"):
                        if item.endswith(".idx"):
                            os.remove(f"{model}/{item}")

            else:
                print(f"Data in {model} folder is old. Downloading Latest Data...")

                for file in os.listdir(f"{model}"):
                    try:
                        os.remove(f"{model}/{file}")
                    except Exception as e:
                        pass
                
                for i in range(0, 102, 3):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}/geavg.t{run}z.pgrb2s.0p25.f00{i}", f"geavg.t{run}z.pgrb2s.0p25.f00{i}")
                        os.replace(f"geavg.t{run}z.pgrb2s.0p25.f00{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25.f00{i}")
                    else:
                        urllib.request.urlretrieve(f"{url}/geavg.t{run}z.pgrb2s.0p25.f0{i}", f"geavg.t{run}z.pgrb2s.0p25.f0{i}")
                        os.replace(f"geavg.t{run}z.pgrb2s.0p25.f0{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25.f0{i}")
                for i in range(102, 243, 3):
                    urllib.request.urlretrieve(f"{url}/geavg.t{run}z.pgrb2s.0p25.f{i}", f"geavg.t{run}z.pgrb2s.0p25.f{i}")
                    os.replace(f"geavg.t{run}z.pgrb2s.0p25.f{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25.f{i}")                
            

        else:
            print(f"Setting Up The Folder and downloading the files.")
            os.mkdir(f"{model}")
            for i in range(0, 102, 3):
                if i < 10:
                    urllib.request.urlretrieve(f"{url}/geavg.t{run}z.pgrb2s.0p25.f00{i}", f"geavg.t{run}z.pgrb2s.0p25.f00{i}")
                    os.replace(f"geavg.t{run}z.pgrb2s.0p25.f00{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25.f00{i}")
                else:
                    urllib.request.urlretrieve(f"{url}/geavg.t{run}z.pgrb2s.0p25.f0{i}", f"geavg.t{run}z.pgrb2s.0p25.f0{i}")
                    os.replace(f"geavg.t{run}z.pgrb2s.0p25.f0{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25.f0{i}")
            for i in range(102, 243, 3):
                urllib.request.urlretrieve(f"{url}/geavg.t{run}z.pgrb2s.0p25.f{i}", f"geavg.t{run}z.pgrb2s.0p25.f{i}")
                os.replace(f"geavg.t{run}z.pgrb2s.0p25.f{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25.f{i}")
    
        for i in range(0, 102, 3):
            if i < 10:
                try:
                    os.replace(f"{model}/geavg.t{run}z.pgrb2s.0p25.f00{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25_f00{i}.grib2")
                except Exception as e:
                    pass
            else:
                try:
                    os.replace(f"{model}/geavg.t{run}z.pgrb2s.0p25.f0{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25_f0{i}.grib2")
                except Exception as e:
                    pass
        
        for i in range(102, 243, 3):
            try:
                os.replace(f"{model}/geavg.t{run}z.pgrb2s.0p25.f{i}", f"{model}/geavg.t{run}z.pgrb2s.0p25_f{i}.grib2")
            except Exception as e:
                pass            

        file_pattern = f"{model}/*.grib2"

        if u_and_v_wind == True:
            u = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName': '10u'}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
            v = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName': '10v'}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            u = shift_longitude(u)
            v = shift_longitude(v)

            for item in os.listdir(f"{model}"):
                if item.endswith(".idx"):
                    os.remove(f"{model}/{item}")

            return u, v

        else:
            ds = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': typeOfLevel}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            ds = shift_longitude(ds)

            for item in os.listdir(f"{model}"):
                if item.endswith(".idx"):
                    os.remove(f"{model}/{item}")

            return ds

