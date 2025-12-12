"""
This file hosts functions that download various types of AIGEFS Data

(C) Eric J. Drewitz 2025
"""

import wxdata.client.client as client
import wxdata.post_processors.aigefs_post_processing as aigefs_post_processing
import os
import warnings
warnings.filterwarnings('ignore')

from wxdata.aigefs.url_scanners import(
    aigefs_pres_url_scanner,
    aigefs_sfc_url_scanner
)

from wxdata.utils.file_funcs import custom_branches
from wxdata.aigefs.paths import build_aigefs_directory
from wxdata.calc.unit_conversion import convert_temperature_units
from wxdata.utils.file_scanner import local_file_scanner
from wxdata.utils.recycle_bin import *

def aigefs_pressure_members(final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=True,
            convert_temperature=True,
            convert_to='celsius',
            custom_directory=None,
            chunk_size=8192,
            notifications='off'):
    
    """
    This function downloads the latest pressure parameter dataset of the AIGEFS and bins the files to specific folders based on ensemble number.
    Users can also enter a list of paths for custom_directory if they do not wish to use the default directory.
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
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
    
    7) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
            
    10) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    11) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
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
    
    An xarray data array of the AIGEFS Pressure Parameter data specified to the coordinate boundaries and variable list the user specifies. 
    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass    
    
    if custom_directory == None:
        paths = build_aigefs_directory('pressure',
                                       members)
    else:
        paths = custom_branches(custom_directory)
        
    urls, file, run = aigefs_pres_url_scanner(final_forecast_hour,
                            proxies,
                            members)
    
    download = local_file_scanner(paths[-1], 
                                    file,
                                    'nomads',
                                    run,
                                    model='aigefs')  
    
    if download == True:
        print(f"Downloading AIGEFS Pressure Parameter Files...")
        
        try:
            for path in paths:
                for file in os.listdir(f"{path}"):
                    os.remove(f"{path}/{file}")
        except Exception as e:
            pass
         
        if run < 10:
            run = f"0{run}"
        else:
            run = f"{run}"        
        stop = final_forecast_hour + 6
        for path, url in zip(paths, urls):
            for i in range(0, stop, 6):
                if i < 10:
                    client.get_gridded_data(f"{url}/aigefs.t{run}z.pres.f00{i}.grib2",
                                path,
                                f"aigefs.t{run}z.pres.f00{i}.grib2",
                                proxies=proxies,
                                chunk_size=chunk_size,
                                notifications=notifications)  
                elif i >= 10 and i < 100:
                    client.get_gridded_data(f"{url}/aigefs.t{run}z.pres.f0{i}.grib2",
                                path,
                                f"aigefs.t{run}z.pres.f0{i}.grib2",
                                proxies=proxies,
                                chunk_size=chunk_size,
                                notifications=notifications)  
                else:
                    client.get_gridded_data(f"{url}/aigefs.t{run}z.pres.f{i}.grib2",
                                path,
                                f"aigefs.t{run}z.pres.f{i}.grib2",
                                proxies=proxies,
                                chunk_size=chunk_size,
                                notifications=notifications)     
    else:
        print(f"User has latest AIGEFS Pressure Parameter Files\nSkipping Download...")  
        
    if process_data == True:
        print(f"AIGEFS Pressure Parameters Data Processing...")    
        
        ds = aigefs_post_processing.aigefs_members_post_processing(paths,
                                                                    western_bound,
                                                                    eastern_bound,
                                                                    northern_bound,
                                                                    southern_bound)
        
        if convert_temperature == True:
            ds = convert_temperature_units(ds, 
                                           convert_to, 
                                           cat='mean')
                
        
        print(f"AIGEFS Pressure Parameters Data Processing Complete.")
        return ds
    else:
        pass           
                        
                        

def aigefs_surface_members(final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=True,
            convert_temperature=True,
            convert_to='celsius',
            custom_directory=None,
            chunk_size=8192,
            notifications='off'):
    
    """
    This function downloads the latest surface parameter dataset of the AIGEFS and bins the files to specific folders based on ensemble number.
    Users can also enter a list of paths for custom_directory if they do not wish to use the default directory.
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
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
    
    7) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
            
    10) custom_directory (String, String List or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. If cat='members' then the user must pass in a string list showing the filepaths for each set of files binned by ensemble member.
    
    11) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
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
    
    An xarray data array of the AIGEFS Surface Parameter data specified to the coordinate boundaries and variable list the user specifies. 
    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass    
    
    if custom_directory == None:
        paths = build_aigefs_directory('surface',
                                       members)
    else:
        paths = custom_branches(custom_directory)
        
    urls, file, run = aigefs_sfc_url_scanner(final_forecast_hour,
                            proxies,
                            members)
    
    download = local_file_scanner(paths[-1], 
                                    file,
                                    'nomads',
                                    run,
                                    model='aigefs')  
    
    if download == True:
        print(f"Downloading AIGEFS Surface Parameter Files...")
        
        try:
            for path in paths:
                for file in os.listdir(f"{path}"):
                    os.remove(f"{path}/{file}")
        except Exception as e:
            pass
         
        if run < 10:
            run = f"0{run}"
        else:
            run = f"{run}"        
        stop = final_forecast_hour + 6
        for path, url in zip(paths, urls):
            for i in range(0, stop, 6):
                if i < 10:
                    client.get_gridded_data(f"{url}/aigefs.t{run}z.sfc.f00{i}.grib2",
                                path,
                                f"aigefs.t{run}z.sfc.f00{i}.grib2",
                                proxies=proxies,
                                chunk_size=chunk_size,
                                notifications=notifications)  
                elif i >= 10 and i < 100:
                    client.get_gridded_data(f"{url}/aigefs.t{run}z.sfc.f0{i}.grib2",
                                path,
                                f"aigefs.t{run}z.sfc.f0{i}.grib2",
                                proxies=proxies,
                                chunk_size=chunk_size,
                                notifications=notifications)  
                else:
                    client.get_gridded_data(f"{url}/aigefs.t{run}z.sfc.f{i}.grib2",
                                path,
                                f"aigefs.t{run}z.sfc.f{i}.grib2",
                                proxies=proxies,
                                chunk_size=chunk_size,
                                notifications=notifications)    
                    
    else:
        print(f"User has latest AIGEFS Surface Parameter Files\nSkipping Download...")  
        
    if process_data == True:
        print(f"AIGEFS Surface Parameters Data Processing...")    
        
        ds = aigefs_post_processing.aigefs_members_post_processing(paths,
                                                                    western_bound,
                                                                    eastern_bound,
                                                                    northern_bound,
                                                                    southern_bound)
        
        if convert_temperature == True:
            ds = convert_temperature_units(ds, 
                                           convert_to, 
                                           cat='mean')
                
        
        print(f"AIGEFS Surface Parameters Data Processing Complete.")
        return ds
    else:
        pass   