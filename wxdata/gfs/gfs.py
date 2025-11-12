"""
This file hosts the functions the user interacts with to download GFS data. 

(C) Eric J. Drewitz 2025
"""

import wxdata.client.client as client
import os
import warnings
import wxdata.utils.gefs_post_processing as gefs_post_processing
warnings.filterwarnings('ignore')

from wxdata.gfs.paths import build_directory
from wxdata.gfs.url_scanners import(
    
    gfs_0p50_url_scanner,
    gfs_0p25_url_scanner,
    gfs_0p25_secondary_parameters_url_scanner
)


from wxdata.utils.file_funcs import custom_branch

#from wxdata.calc.derived_fields import gefs_primary_derived_fields
from wxdata.calc.unit_conversion import convert_temperature_units
from wxdata.utils.file_scanner import local_file_scanner
from wxdata.utils.recycle_bin import *


def gfs_0p25(final_forecast_hour=384, 
            western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            step=3,
            process_data=True,
            proxies=None, 
            variables=['best lifted index',
                       'absolute vorticity',
                       'convective precipitation',
                       'albedo',
                       'total precipitation',
                       'convective available potential energy',
                       'categorical freezing rain',
                       'categorical ice pellets',
                       'convective inhibition',
                       'cloud mixing ratio',
                       'plant canopy surface water',
                       'percent frozen precipitaion',
                       'convective precipitation rate',
                       'categorical rain',
                       'categorical snow',
                       'cloud water',
                       'cloud work function',
                       'downward longwave radiation flux',
                       'dew point',
                       'downward shortwave radiation flux',
                       'vertical velocity (height)',
                       'field capacity',
                       'surface friction velocity',
                       'ground heat flux',
                       'graupel',
                       'wind gust',
                       'high cloud cover',
                       'geopotential height',
                       'haines index',
                       'storm relative helicity',
                       'planetary boundary layer height',
                       'icao standard atmosphere reference height',
                       'ice cover',
                       'ice growth rate',
                       'ice thickness',
                       'ice temperature',
                       'ice water mixing ratio',
                       'land cover',
                       'low cloud cover',
                       'surface lifted index',
                       'latent heat net flux',
                       'middle cloud cover',
                       'mslp (eta model reduction)',
                       'ozone mixing ratio',
                       'potential evaporation rate',
                       'pressure level from which parcel was lifted',
                       'potential temperature',
                       'precipitation rate',
                       'pressure',
                       'mean sea level pressure',
                       'precipitable water',
                       'composite reflectivity',
                       'reflectivity',
                       'relative humidity',
                       'rain mixing ratio',
                       'surface roughness',
                       'sensible heat net flux',
                       'snow mixing ratio',
                       'snow depth',
                       'liquid volumetric soil moisture (non-frozen)',
                       'volumetric soil moisture content',
                       'soil type',
                       'specific humidity',
                       'sunshine duration',
                       'total cloud cover',
                       'maximum temperature',
                       'minimum temperature',
                       'temperature',
                       'total ozone',
                       'soil temperature',
                       'momentum flux (u-component)',
                       'u-component of wind',
                       'zonal flux of gravity wave stress',
                       'upward longwave radiation flux',
                       'u-component of storm motion',
                       'upward shortwave radiation flux',
                       'vegetation',
                       'momentum flux (v-component)',
                       'v-component of wind',
                       'meridional flux of gravity wave stress',
                       'visibility',
                       'ventilation rate',
                       'v-component of storm motion',
                       'vertical velocity (pressure)',
                       'vertical speed shear',
                       'water runoff',
                       'water equivalent of accumulated snow depth',
                       'wilting point'],
            custom_directory=None,
            clear_recycle_bin=True,
            chunk_size=8192,
            notifications='off'):
    
    """
    This function downloads GFS data and saves it to a folder. 
    
    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    if custom_directory==None:
        path = build_directory('gfs0p25',
                               'atmospheric')
        
    else:
        try:
            os.makedirs(f"{custom_directory}")
        except Exception as e:
            pass
        
        path = custom_directory
        
    urls, filenames, run = gfs_0p25_url_scanner(final_forecast_hour,
                                            western_bound, 
                                            eastern_bound, 
                                            northern_bound, 
                                            southern_bound, 
                                            proxies, 
                                            step, 
                                            variables)
    
    download = local_file_scanner(path, 
                                    filenames[-1],
                                    'nomads',
                                    run)   
    
    if download == True:
        print(f"Data downloading...")
        
        try:
            for file in os.listdir(f"{path}"):
                os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        for url, filename in zip(urls, filenames):
            client.get_gridded_data(f"{url}",
                        path,
                        f"{filename}.grib2",
                        proxies=proxies,
                        chunk_size=chunk_size,
                        notifications=notifications)   
            
    else:
        print(f"User has the current dataset.\nSkipping download.")
    
    
    
    
    
def gfs_0p25_secondary_parameters(final_forecast_hour=384, 
            western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            step=3,
            process_data=True,
            proxies=None, 
            variables=['absolute vorticity',
                       'clear sky uv-b downward solar flux',
                       'cloud mixing ratio',
                       'plant canopy surface water',
                       'uv-b downward solar flux',
                       'vertical velocity (height)',
                       'graupel',
                       'geopotential height',
                       'ice thickness',
                       'ice water mixing ratio',
                       'ozone mixing ratio',
                       'pressure',
                       'relative humidity',
                       'rain mixing ratio',
                       'snow mixing ratio',
                       'liquid volumetric soil moisture (non-frozen)',
                       'specific humidity',
                       'total cloud cover',
                       'temperature',
                       'u-component of wind',
                       'v-component of wind',
                       'vertical velocity (pressure)',
                       'vertical speed shear'],
            custom_directory=None,
            clear_recycle_bin=True,
            chunk_size=8192,
            notifications='off'):
    
    """
    This function downloads GFS data and saves it to a folder. 
    
    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    if custom_directory==None:
        path = build_directory('gfs0p25 secondary parameters',
                               'atmospheric')
        
    else:
        try:
            os.makedirs(f"{custom_directory}")
        except Exception as e:
            pass
        
        path = custom_directory
        
    urls, filenames, run = gfs_0p25_secondary_parameters_url_scanner(final_forecast_hour,
                                            western_bound, 
                                            eastern_bound, 
                                            northern_bound, 
                                            southern_bound, 
                                            proxies, 
                                            step, 
                                            variables)
    
    download = local_file_scanner(path, 
                                    filenames[-1],
                                    'nomads',
                                    run)   
    
    if download == True:
        print(f"Data downloading...")
        
        try:
            for file in os.listdir(f"{path}"):
                os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        for url, filename in zip(urls, filenames):
            client.get_gridded_data(f"{url}",
                        path,
                        f"{filename}.grib2",
                        proxies=proxies,
                        chunk_size=chunk_size,
                        notifications=notifications)   
            
    else:
        print(f"User has the current dataset.\nSkipping download.")
        
        
def gfs_0p50(final_forecast_hour=384, 
            western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            step=3,
            process_data=True,
            proxies=None, 
            variables=['best lifted index',
                       'absolute vorticity',
                       'convective precipitation',
                       'albedo',
                       'total precipitation',
                       'convective available potential energy',
                       'categorical freezing rain',
                       'categorical ice pellets',
                       'convective inhibition',
                       'cloud mixing ratio',
                       'plant canopy surface water',
                       'percent frozen precipitaion',
                       'convective precipitation rate',
                       'categorical rain',
                       'categorical snow',
                       'cloud water',
                       'cloud work function',
                       'downward longwave radiation flux',
                       'dew point',
                       'downward shortwave radiation flux',
                       'vertical velocity (height)',
                       'field capacity',
                       'surface friction velocity',
                       'ground heat flux',
                       'graupel',
                       'wind gust',
                       'high cloud cover',
                       'geopotential height',
                       'haines index',
                       'storm relative helicity',
                       'planetary boundary layer height',
                       'icao standard atmosphere reference height',
                       'ice cover',
                       'ice growth rate',
                       'ice thickness',
                       'ice temperature',
                       'ice water mixing ratio',
                       'land cover',
                       'low cloud cover',
                       'surface lifted index',
                       'latent heat net flux',
                       'middle cloud cover',
                       'mslp (eta model reduction)',
                       'ozone mixing ratio',
                       'potential evaporation rate',
                       'pressure level from which parcel was lifted',
                       'potential temperature',
                       'precipitation rate',
                       'pressure',
                       'mean sea level pressure',
                       'precipitable water',
                       'composite reflectivity',
                       'reflectivity',
                       'relative humidity',
                       'rain mixing ratio',
                       'surface roughness',
                       'sensible heat net flux',
                       'snow mixing ratio',
                       'snow depth',
                       'liquid volumetric soil moisture (non-frozen)',
                       'volumetric soil moisture content',
                       'soil type',
                       'specific humidity',
                       'sunshine duration',
                       'total cloud cover',
                       'maximum temperature',
                       'minimum temperature',
                       'temperature',
                       'total ozone',
                       'soil temperature',
                       'momentum flux (u-component)',
                       'u-component of wind',
                       'zonal flux of gravity wave stress',
                       'upward longwave radiation flux',
                       'u-component of storm motion',
                       'upward shortwave radiation flux',
                       'vegetation',
                       'momentum flux (v-component)',
                       'v-component of wind',
                       'meridional flux of gravity wave stress',
                       'visibility',
                       'ventilation rate',
                       'v-component of storm motion',
                       'vertical velocity (pressure)',
                       'vertical speed shear',
                       'water runoff',
                       'water equivalent of accumulated snow depth',
                       'wilting point',
                       'clear sky uv-b downward solar flux',
                       'uv-b downward solar flux'],
            custom_directory=None,
            clear_recycle_bin=True,
            chunk_size=8192,
            notifications='off'):
    
    """
    This function downloads GFS data and saves it to a folder. 
    
    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    if custom_directory==None:
        path = build_directory('gfs0p50',
                               'atmospheric')
        
    else:
        try:
            os.makedirs(f"{custom_directory}")
        except Exception as e:
            pass
        
        path = custom_directory
        
    urls, filenames, run = gfs_0p50_url_scanner(final_forecast_hour,
                                            western_bound, 
                                            eastern_bound, 
                                            northern_bound, 
                                            southern_bound, 
                                            proxies, 
                                            step, 
                                            variables)
    
    download = local_file_scanner(path, 
                                    filenames[-1],
                                    'nomads',
                                    run)   
    
    if download == True:
        print(f"Data downloading...")
        
        try:
            for file in os.listdir(f"{path}"):
                os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        for url, filename in zip(urls, filenames):
            client.get_gridded_data(f"{url}",
                        path,
                        f"{filename}.grib2",
                        proxies=proxies,
                        chunk_size=chunk_size,
                        notifications=notifications)   
            
    else:
        print(f"User has the current dataset.\nSkipping download.")