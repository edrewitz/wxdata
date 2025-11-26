"""
This file hosts the function that downloads and returns RTMA Data from the NCEP/NOMADS Server. 

(C) Eric J. Drewitz 2025
"""
import os
import warnings
import wxdata.client.client as client
warnings.filterwarnings('ignore')

from wxdata.rtma.file_funcs import(
     build_directory,
     clear_idx_files
)

from wxdata.rtma.url_scanners import(
    rtma_url_scanner,
    rtma_comparison_url_scanner
)

from wxdata.utils.file_funcs import custom_branch
from wxdata.calc.derived_fields import rtma_derived_fields
from wxdata.utils.file_scanner import local_file_scanner
from wxdata.calc.unit_conversion import convert_temperature_units
from wxdata.rtma.process import process_rtma_data
from wxdata.utils.recycle_bin import *

def bounds(model):
    
    """
    This function determines the boundaries for the data based on the region.
    
    Required Arguments: 
    
    1) model (String) - The RTMA model being used. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    The bounding box for the data.     
    """
    
    models = {
        
        'RTMA':[-125, -65, 20, 50],
        'HI RTMA':[-180, 180, -90, 90],
        'PR RTMA':[-68, -65, 17, 19],
        'GU RTMA':[-180, 180, -90, 90],
        'AK RTMA':[-180, -120, 45, 75]
        
    }
    
    return models[model][0], models[model][1], models[model][2], models[model][3]

def rtma(model='rtma', 
         cat='analysis', 
         proxies=None,
         process_data=True,
         clear_recycle_bin=True,
         western_bound=None,
         eastern_bound=None,
         southern_bound=None,
         northern_bound=None,
         convert_temperature=True,
         convert_to='fahrenheit',
         custom_directory=None,
         clear_data=False,
         chunk_size=8192,
         notifications='off'):
    
    """
    This function downloads the latest RTMA Dataset and returns it as an xarray data array. 
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) model (String) - Default='rtma'. The RTMA model being used:
    
    RTMA Models
    -----------
    
    CONUS = 'rtma'
    Alaska = 'ak rtma'
    Hawaii = 'hi rtma'
    Puerto Rico = 'pr rtma'
    Guam = 'gu rtma'
    
    2) cat (String) - Default='analysis'. The category of the RTMA dataset. 
    
    RTMA Categories
    ---------------
    
    analysis - Latest RTMA Analysis
    error - Latest RTMA Error
    surface 1 hour forecast - RTMA Surface 1 Hour Forecast
    
    3) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                        }
                        
    4) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    5) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    6) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    7) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    8) southern_bound (Float or Integer) - Default=-90. The northern bound of the data needed.

    9) northern_bound (Float or Integer) - Default=90. The southern bound of the data needed.
    
    10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    12) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
        
    13) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    14) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    Returns
    -------
    
    An xarray data array of the RTMA Dataset with variable keys converted from the GRIB format to a Plain Language format. 
    
    Variable Keys
    -------------
    
    'orography'
    'surface_pressure'
    '2m_temperature'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_specific_humidity'
    'surface_visibility'
    'cloud_ceiling_height'
    'total_cloud_cover'
    '10m_u_wind_component'
    '10m_v_wind_component'
    '10m_wind_direction'
    '10m_wind_speed'
    '10m_wind_gust'
    '2m_apparent_temperature'
    '2m_dew_point_depression'
    
    """
    
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    
    model = model.upper()
    cat = cat.upper()
    
    if custom_directory == None:
        path = build_directory(model,
                            cat)
    else:
        path = custom_branch(custom_directory)
    
    clear_idx_files(path)
    
    if western_bound == None and eastern_bound == None and southern_bound == None and northern_bound == None:
        western_bound, eastern_bound, southern_bound, northern_bound = bounds(model)
    else:
        western_bound = western_bound
        eastern_bound = eastern_bound 
        southern_bound = southern_bound 
        northern_bound = northern_bound
            
    try:
        files = []
        for file in os.listdir(f"{path}"):
            files.append(file)
        if len(files) > 2:
            for file in os.listdir(f"{path}"):
                os.remove(f"{path}/{file}")
        else:
            pass
    except Exception as e:
        pass
    
    url, filename, run = rtma_url_scanner(model, 
                    cat,
                    western_bound, 
                    eastern_bound, 
                    northern_bound, 
                    southern_bound, 
                    proxies)
    
    print(filename)
    
    download = local_file_scanner(path, 
                                filename,
                                'nomads',
                                run) 
    
    if clear_data == True:
        download = True
    else:
        pass
    
    if download == True:
        print(f"Data Downloading...")
        
        try:
            for file in os.listdir(f"{path}"):
                os.remove(f"{path}/{file}")
        except Exception as e:
            pass

        client.get_gridded_data(f"{url}", 
                    path,
                    f"{filename}.grib2",
                    proxies=proxies,
                    chunk_size=chunk_size,
                    notifications=notifications)
        
        print(f"Download Complete.")
    else:
        print(f"{model} Data is current. Skipping download.")
        
    if process_data == True:
        print(f"Data Processing...")
        filename = f"{filename}.grib2"
        ds = process_rtma_data(path, 
                                filename, 
                                model)
        
        
        if convert_temperature == True:
            try:
                ds = convert_temperature_units(ds, 
                                                convert_to)
            except Exception as e:
                pass
            
        else:
            pass
        
        ds = rtma_derived_fields(ds,
                                convert_temperature,
                                convert_to)

        clear_idx_files(path)
        
        print(f"Data Processing Complete.")
        return ds
    
    else:
        pass
        
    
def rtma_comparison(model='rtma', 
         cat='analysis', 
         hours=24,
         proxies=None,
         process_data=True,
         clear_recycle_bin=True,
         western_bound=None,
         eastern_bound=None,
         southern_bound=None,
         northern_bound=None,
         clear_data=False,
         convert_temperature=True,
         convert_to='fahrenheit',
         custom_directory=None,
         chunk_size=8192,
         notifications='off'):
    
    """
    This function downloads the latest RTMA Dataset and the RTMA dataset from 24 hours prior to the current RTMA dataset and returns it as two xarray data arrays. 
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) model (String) - Default='rtma'. The RTMA model being used:
    
    RTMA Models
    -----------
    
    CONUS = 'rtma'
    Alaska = 'ak rtma'
    Hawaii = 'hi rtma'
    Puerto Rico = 'pr rtma'
    Guam = 'gu rtma'
    
    2) cat (String) - Default='analysis'. The category of the RTMA dataset. 
    
    RTMA Categories
    ---------------
    
    analysis - Latest RTMA Analysis
    error - Latest RTMA Error
    surface 1 hour forecast - RTMA Surface 1 Hour Forecast
    
    3) hours (Integer) - Default=24. The amount of hours previous to the current dataset for the comparison dataset. 
    
    4) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                        }
                        
    5) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    6) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    7) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    8) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    9) southern_bound (Float or Integer) - Default=-90. The northern bound of the data needed.

    10) northern_bound (Float or Integer) - Default=90. The southern bound of the data needed.
    
    11) clear_data (Boolean) - Default=False. When set to True, the current data in the folder is deleted
        and new data is downloaded automatically with each run. 
        This setting is recommended for users who wish to use a medley of different comparisons. 
        
    12) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    13) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    14) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
        
    15) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    16) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    Returns
    -------
    
    1) ds - The current RTMA dataset
    
    2) ds_dt - The RTMA comparison dataset from a user specified amount of hours prior to the current dataset. 
    
    All with variable keys converted from the GRIB format to a Plain Language format. 
    
    Variable Keys
    -------------
    
    'orography'
    'surface_pressure'
    '2m_temperature'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_specific_humidity'
    'surface_visibility'
    'cloud_ceiling_height'
    'total_cloud_cover'
    '10m_u_wind_component'
    '10m_v_wind_component'
    '10m_wind_direction'
    '10m_wind_speed'
    '10m_wind_gust'
    '2m_apparent_temperature'
    '2m_dew_point_depression'
    
    """
    
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    
    model = model.upper()
    cat = cat.upper()
    
    if custom_directory == None:
        path = build_directory(model,
                            cat)
    else:
        path = custom_branch(custom_directory)
    
    clear_idx_files(path)
    
    try:
        files = []
        for file in os.listdir(f"{path}"):
            files.append(file)
        if len(files) > 2:
            for file in os.listdir(f"{path}"):
                os.remove(f"{path}/{file}")
        else:
            pass
    except Exception as e:
        pass
    
    if western_bound == None and eastern_bound == None and southern_bound == None and northern_bound == None:
        western_bound, eastern_bound, southern_bound, northern_bound = bounds(model)
    else:
        western_bound = western_bound
        eastern_bound = eastern_bound 
        southern_bound = southern_bound 
        northern_bound = northern_bound
    
    url, url_dt, filename, filename_dt, run = rtma_comparison_url_scanner(model, 
                    cat,
                    western_bound, 
                    eastern_bound, 
                    northern_bound, 
                    southern_bound, 
                    proxies,
                    hours)
    
    download = local_file_scanner(path, 
                                filename,
                                source='nomads',
                                run=run) 
    
    if clear_data == True:
        download = True
    else:
        pass
    
    if download == True:
        
        try:
            for file in os.listdir(f"{path}"):
                os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        print(f"Data Downloading...")
        client.get_gridded_data(f"{url}", 
                    path,
                    f"{filename}.grib2",
                    proxies=proxies,
                    chunk_size=chunk_size,
                    notifications=notifications)
        client.get_gridded_data(f"{url_dt}", 
                    path,
                    f"{filename_dt}.grib2",
                    proxies=proxies,
                    chunk_size=chunk_size,
                    notifications=notifications)
        print(f"Download Complete.")
    else:
        print(f"{model} Data is current. Skipping download.")
        
    if process_data == True:
        print(f"Data Processing...")
        filename = f"{filename}.grib2"
        ds = process_rtma_data(path, 
                                filename, 
                                model)
        
        filename_dt = f"{filename_dt}.grib2"
        ds_dt = process_rtma_data(path, 
                                filename_dt, 
                                model)
        
        if convert_temperature == True:
            ds = convert_temperature_units(ds, 
                                            convert_to)
            
            ds_dt = convert_temperature_units(ds_dt, 
                                            convert_to)
            
        else:
            pass
            
        ds = rtma_derived_fields(ds,
                            convert_temperature,
                            convert_to)
            
        ds_dt = rtma_derived_fields(ds_dt,
                            convert_temperature,
                            convert_to)


        clear_idx_files(path)
        
        print(f"Data Processing Complete.")
        return ds, ds_dt
    
    else:
        pass
        
    
    
    