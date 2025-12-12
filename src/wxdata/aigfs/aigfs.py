"""
This file hosts the clients that download, pre-process and post-process AIGFS Data.

(C) Eric J. Drewitz 2025
"""

import wxdata.client.client as client
import wxdata.post_processors.aigfs_post_processing as aigfs_post_processing
import os
import warnings
warnings.filterwarnings('ignore')

from wxdata.aigfs.url_scanners import aigfs_url_scanner
from wxdata.aigfs.paths import build_aigfs_directory
from wxdata.utils.file_funcs import custom_branch
from wxdata.calc.unit_conversion import convert_temperature_units
from wxdata.utils.file_scanner import local_file_scanner
from wxdata.utils.recycle_bin import *


def aigfs(final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             process_data=True,
             clear_recycle_bin=True,
            convert_temperature=True,
            convert_to='celsius',
            custom_directory=None,
            chunk_size=8192,
            notifications='off',
            type_of_level='pressure'):
    
    """
    This function downloads, pre-processes and post-processes the latest AIGFS Data. 
    Users can also enter a list of paths for custom_directory if they do not wish to use the default directory.
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The AIGEFS
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    6) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
    
    7) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    8) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
            
    9) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    10) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    11) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    12) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    13) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
        
    14) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    15) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    16) type_of_level (String) - Default='pressure'. The type of level the data is in.
    
        Types of Levels
        ---------------
        
        1) pressure
        2) surface
    
    
    Returns
    -------
    
    An xarray data array of the AIGEFS data specified to the coordinate boundaries and variable list the user specifies. 
    
    Pressure-Level Plain Language Variable Keys
    -------------------------------------------
    
    'geopotential_height'
    'specific_humidity'
    'air_temperature'
    'u_wind_component'
    'v_wind_component'
    'vertical_velocity'
    
    Surface-Level Plain Language Variable Keys
    ------------------------------------------
    
    '10m_u_wind_component'
    '10m_v_wind_component'
    'mslp'
    '2m_temperature'
    """
    
    type_of_level = type_of_level.lower()
    
    if type_of_level == 'pressure':
        level = 'pres'
    else:
        level = 'sfc'
    
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass   
    
    if custom_directory == None:
        path = build_aigfs_directory(type_of_level)
    else:
        path = custom_branch(custom_directory)
        
    url, file, run = aigfs_url_scanner(final_forecast_hour,
                                                        proxies,
                                                        type_of_level)
    
    download = local_file_scanner(path, 
                                    file,
                                    'nomads',
                                    run,
                                    model='aigfs')  
    
    
    if download == True:
        print(f"Downloading AIGFS {type_of_level.upper()} Files...")
        
        try:
            for file in os.listdir(f"{path}"):
                os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        if run < 10:
            run = f"0{run}"
        else:
            run = f"{run}"        
        stop = final_forecast_hour + 6
        
        for i in range(0, stop, 6):
            if i < 10:
                client.get_gridded_data(f"{url}aigfs.t{run}z.{level}.f00{i}.grib2",
                            path,
                            f"aigfs.t{run}z.{level}.f00{i}.grib2",
                            proxies=proxies,
                            chunk_size=chunk_size,
                            notifications=notifications)  
            elif i >= 10 and i < 100:
                client.get_gridded_data(f"{url}aigfs.t{run}z.{level}.f0{i}.grib2",
                            path,
                            f"aigfs.t{run}z.{level}.f0{i}.grib2",
                            proxies=proxies,
                            chunk_size=chunk_size,
                            notifications=notifications)  
            else:
                client.get_gridded_data(f"{url}aigfs.t{run}z.{level}.f{i}.grib2",
                            path,
                            f"aigfs.t{run}z.{level}.f{i}.grib2",
                            proxies=proxies,
                            chunk_size=chunk_size,
                            notifications=notifications)    
                    
    else:
        print(f"User has latest AIGFS {type_of_level.upper()} Files\nSkipping Download...")  
    
    if process_data == True:
        print(f"AIGFS {type_of_level.upper()} Data Processing...")    
        
        ds = aigfs_post_processing.aigfs_post_processing(path,
                                                        western_bound,
                                                        eastern_bound,
                                                        northern_bound,
                                                        southern_bound)
        
        if convert_temperature == True:
            ds = convert_temperature_units(ds, 
                                           convert_to, 
                                           cat='mean')
                
        
        print(f"AIGFS {type_of_level.upper()} Data Processing Complete.")
        return ds
    else:
        pass    


