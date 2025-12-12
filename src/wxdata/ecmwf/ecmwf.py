"""
This file hosts the functions the user has to download ECMWF model data. 

(C) Eric J. Drewitz 2025
"""

import warnings
import wxdata.client.client as client
import wxdata.post_processors.ecmwf_post_processing as ecmwf_post_processing
warnings.filterwarnings('ignore')

from wxdata.ecmwf.url_scanners import(
    ecmwf_ifs_url_scanner, 
    ecmwf_aifs_url_scanner,
    ecmwf_ifs_high_res_url_scanner,
    ecmwf_ifs_wave_url_scanner
)

from wxdata.ecmwf.file_funcs import(
    build_directory,
    clear_idx_files,
    clear_old_data,
    parse_filename
)


from wxdata.calc.unit_conversion import convert_temperature_units
from wxdata.utils.file_scanner import local_file_scanner
from wxdata.ecmwf.paths import ecmwf_branch_paths
from wxdata.utils.file_funcs import(
    custom_branch,
    clear_idx_files_in_path
)
from wxdata.utils.recycle_bin import *


def ecmwf_ifs(final_forecast_hour=360,
              western_bound=-180,
              eastern_bound=180,
              northern_bound=90,
              southern_bound=-90,
              step=3,
              proxies=None,
              process_data=True,
              clear_recycle_bin=True,
              convert_temperature=True,
              convert_to='celsius',
              custom_directory=None,
              chunk_size=8192,
              notifications='off'):
    
    """
    This function scans for the latest ECMWF IFS dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 360. The final forecast hour the user wishes to download. The ECMWF IFS
    goes out to 360 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    360 by the nereast increment of 3 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
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
    
    An xarray data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF IFS Variable Keys (After Post-Processing)
    --------------------------------------------------------------
    
    'total_column_water'
    'total_column_vertically_integrated_water_vapor'
    'snow_albedo'
    'land_sea_mask'
    'specific_humidity'
    'volumetric_soil_moisture_content'
    'sea_ice_thickness'
    'soil_temperature'
    'surface_longwave_radiation_downward'
    'surface_net_shortwave_solar_radiation'
    'surface_net_longwave_thermal_radiation'
    'top_net_longwave_thermal_radiation'
    '10m_max_wind_gust'
    'vertical_velocity'
    'relative_vorticity'
    'relative_humidity'
    'geopotential_height'
    'eastward_turbulent_surface_stress'
    'u_wind_component'
    'divergence'
    'northward_turbulent_surface_stress'
    'v_wind_component'
    'air_temperature'
    'water_runoff'
    'total_precipitation'
    'mslp'
    'eastward_surface_sea_water_velocity'
    'most_unstable_cape'
    'northward_surface_sea_water_velocity'
    'sea_surface_height'
    'standard_deviation_of_sub_gridscale_orography'
    'skin_temperature'
    'slope_of_sub_gridscale_orography'
    '10m_u_wind_component'
    'precipitation_type'
    '10m_v_wind_component'
    'total_precipitation_rate'
    'surface_shortwave_radiation_downward'
    'geopotential'
    'surface_pressure'
    '2m_temperature'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '2m_dew_point'
    '2m_relative_humidity'
    
    """
    
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    if custom_directory == None:
        build_directory('ifs', 
                        'operational')
        
        path = ecmwf_branch_paths('ifs', 
                        'operational')
        
    else:
        path = custom_branch(custom_directory)
    
    clear_idx_files(path)
    
    url, filename, run = ecmwf_ifs_url_scanner(final_forecast_hour,
                          proxies)

    download = local_file_scanner(path, 
                                  filename,
                                  'ecmwf',
                                  run,
                                  model='operational ifs')
    

    date = parse_filename(filename)
    
    if download == True:
        print(f"Downloading ECMWF IFS...")
        clear_old_data(path)
        if final_forecast_hour <= 144:
            for i in range(0, final_forecast_hour + step, step):
                client.get_gridded_data(f"{url}/{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2", 
                            path,
                            f"{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2",
                            proxies=proxies,
                            chunk_size=chunk_size,
                            notifications=notifications)
                                              
        else:
            for i in range(0, 144 + step, step):
                client.get_gridded_data(f"{url}/{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2", 
                            path,
                            f"{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2",
                            proxies=proxies,
                            chunk_size=chunk_size,
                            notifications=notifications)
            
            for i in range(144, final_forecast_hour + 6, 6):
                client.get_gridded_data(f"{url}/{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2", 
                            path,
                            f"{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2",
                            proxies=proxies,
                            chunk_size=chunk_size,
                            notifications=notifications)

        
        print(f"ECMWF IFS Download Complete.")    
        
    else:
        print(f"ECMWF IFS Data is up to date. Skipping download...")    
        
        
    if process_data == True:
        print(f"ECMWF IFS Data Processing...")
        
        ds = ecmwf_post_processing.ecmwf_ifs_post_processing(path,
                                                            western_bound, 
                                                            eastern_bound, 
                                                            northern_bound, 
                                                            southern_bound)
        
        clear_idx_files_in_path(path)
            
        if convert_temperature == True:
                ds = convert_temperature_units(ds, 
                                            convert_to)
                
        else:
            pass
        
        print(f"ECMWF IFS Data Processing Complete.")
        return ds
    
    else:
        pass


def ecmwf_aifs(final_forecast_hour=360,
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
              notifications='off'):
    
    """
    This function scans for the latest ECMWF AIFS dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 360. The final forecast hour the user wishes to download. The ECMWF AIFS
    goes out to 360 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    360 by the nereast increment of 6 hours. 
    
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
        
    9) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    10) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    11) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
        
    12) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    Returns
    -------
    
    An xarray data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF AIFS Variable Keys (After Post-Processing) 
    ---------------------------------------------------------------
    
    'volumetric_soil_moisture_content'
    'soil_temperature'
    'geopotential_height'
    'specific_humidity'
    'u_wind_component'
    'v_wind_component'
    'air_temperature'
    'vertical velocity'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '10m_u_wind_component'
    '10m_v_wind_component'
    '2m_temperature'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    'water_runoff' 
    'surface_geopotential_height'
    'skin_temperature'
    'surface_pressure'
    'standard_deviation_of_sub_gridscale_orography'
    'slope_of_sub_gridscale_orography'
    'surface_shortwave_radiation_downward'
    'land_sea_mask'
    'surface_longwave_radiation_downward'
    'convective_precipitation'
    'snowfall_water_equivalent'
    'total_precipitation'
    'low_cloud_cover'
    'middle_cloud_cover'
    'high_cloud_cover'
    'total_column_water'
    'total_cloud_cover'
    'mslp'
    
    """
    
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    if custom_directory == None:
        build_directory('aifs', 
                        'operational')
        
        path = ecmwf_branch_paths('aifs', 
                        'operational')
        
    else:
        path = custom_branch(custom_directory)
    
    clear_idx_files(path)
    
    url, filename, run = ecmwf_aifs_url_scanner(final_forecast_hour,
                          proxies)

    download = local_file_scanner(path, 
                                  filename,
                                  'ecmwf',
                                  run)
    

    date = parse_filename(filename)
    
    if download == True:
        print(f"Downloading ECMWF AIFS...")
        clear_old_data(path)
        if final_forecast_hour <= 144:
            for i in range(0, final_forecast_hour + 6, 6):
                client.get_gridded_data(f"{url}/{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2", 
                            path,
                            f"{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2",
                            proxies=proxies,
                            chunk_size=chunk_size,
                            notifications=notifications)
                                              
        else:
            for i in range(0, 144 + 6, 6):
                client.get_gridded_data(f"{url}/{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2", 
                            path,
                            f"{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2",
                            proxies=proxies,
                            chunk_size=chunk_size,
                            notifications=notifications)
            
            for i in range(144, final_forecast_hour + 6, 6):
                client.get_gridded_data(f"{url}/{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2", 
                            path,
                            f"{date.strftime('%Y%m%d%H')}0000-{i}h-oper-fc.grib2",
                            proxies=proxies,
                            chunk_size=chunk_size,
                            notifications=notifications)
            
        print(f"ECMWF AIFS Download Complete.")
    else:
        print(f"ECMWF AIFS Data is up to date. Skipping download...")    
        
        
    if process_data == True:
        print(f"ECMWF AIFS Data Processing...")
        
        ds = ecmwf_post_processing.ecmwf_aifs_post_processing(path,
                                                            western_bound, 
                                                            eastern_bound, 
                                                            northern_bound, 
                                                            southern_bound)
        
        clear_idx_files_in_path(path)
            
        if convert_temperature == True:
                ds = convert_temperature_units(ds, 
                                            convert_to)
                
        else:
            pass
        
        print(f"ECMWF AIFS Data Processing Complete.")
        return ds
    
    else:
        pass
    

def ecmwf_ifs_high_res(final_forecast_hour=144,
              western_bound=-180,
              eastern_bound=180,
              northern_bound=90,
              southern_bound=-90,
              step=3,
              proxies=None,
              process_data=True,
              clear_recycle_bin=True,
              convert_temperature=True,
              convert_to='celsius',
              custom_directory=None,
              chunk_size=8192,
              notifications='off'):
    
    """
    This function scans for the latest ECMWF High Resolution IFS dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 360. The final forecast hour the user wishes to download. The ECMWF High Resolution IFS
    goes out to 144 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    144 by the nereast increment of 3 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
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
    
    An xarray data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF High Resolution IFS Variable Keys (After Post-Processing)
    ------------------------------------------------------------------------------
    
    'total_column_water'
    'total_column_vertically_integrated_water_vapor'
    'snow_albedo'
    'land_sea_mask'
    'specific_humidity'
    'volumetric_soil_moisture_content'
    'sea_ice_thickness'
    'soil_temperature'
    'surface_longwave_radiation_downward'
    'surface_net_shortwave_solar_radiation'
    'surface_net_longwave_thermal_radiation'
    'top_net_longwave_thermal_radiation'
    '10m_max_wind_gust'
    'vertical_velocity'
    'relative_vorticity'
    'relative_humidity'
    'geopotential_height'
    'eastward_turbulent_surface_stress'
    'u_wind_component'
    'divergence'
    'northward_turbulent_surface_stress'
    'v_wind_component'
    'air_temperature'
    'water_runoff'
    'total_precipitation'
    'mslp'
    'eastward_surface_sea_water_velocity'
    'most_unstable_cape'
    'northward_surface_sea_water_velocity'
    'sea_surface_height'
    'standard_deviation_of_sub_gridscale_orography'
    'skin_temperature'
    'slope_of_sub_gridscale_orography'
    '10m_u_wind_component'
    'precipitation_type'
    '10m_v_wind_component'
    'total_precipitation_rate'
    'surface_shortwave_radiation_downward'
    'geopotential'
    'surface_pressure'
    '2m_temperature'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '2m_dew_point'
    '2m_relative_humidity'
    
    """
    
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    if custom_directory == None:
        build_directory('ifs', 
                        'high res')
        
        path = ecmwf_branch_paths('ifs', 
                        'high res')
    else:
        path = custom_branch(custom_directory)
    
    clear_idx_files(path)
    
    url, filename, run = ecmwf_ifs_high_res_url_scanner(final_forecast_hour,
                          proxies)

    download = local_file_scanner(path, 
                                  filename,
                                  'ecmwf',
                                  run)

    date = parse_filename(filename)
    
    if download == True:
        print(f"Downloading ECMWF High Resolution IFS...")
        clear_old_data(path)
        for i in range(0, final_forecast_hour + step, step):
            client.get_gridded_data(f"{url}/{date.strftime('%Y%m%d%H')}0000-{i}h-scda-fc.grib2", 
                        path,
                        f"{date.strftime('%Y%m%d%H')}0000-{i}h-scda-fc.grib2",
                        proxies=proxies,
                        chunk_size=chunk_size,
                        notifications=notifications)
                            
        print(f"ECMWF High Resolution IFS Download Complete")
    else:
        print(f"ECMWF High Resolution IFS Data is up to date. Skipping download...")    
        
        
    if process_data == True:
        print(f"ECMWF High Resolution IFS Data Processing...")
        
        ds = ecmwf_post_processing.ecmwf_ifs_post_processing(path,
                                                            western_bound, 
                                                            eastern_bound, 
                                                            northern_bound, 
                                                            southern_bound)
        
        clear_idx_files_in_path(path)
            
        if convert_temperature == True:
                ds = convert_temperature_units(ds, 
                                            convert_to)
                
        else:
            pass
        
        print(f"ECMWF High Resolution IFS Data Processing Complete.")
        return ds
    
    else:
        pass
    
    
def ecmwf_ifs_wave(final_forecast_hour=144,
              western_bound=-180,
              eastern_bound=180,
              northern_bound=90,
              southern_bound=-90,
              step=3,
              proxies=None,
              process_data=True,
              clear_recycle_bin=True,
              custom_directory=None,
              chunk_size=8192,
              notifications='off'):
    
    """
    This function scans for the latest ECMWF IFS Wave dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 360. The final forecast hour the user wishes to download. The ECMWF IFS Wave
    goes out to 144 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    144 by the nereast increment of 3 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    10) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
        
    11) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    12) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
        
    Returns
    -------
    
    An xarray data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF IFS Wave Variable Keys (After Post-Processing)
    -------------------------------------------------------------------
    
    'mean_zero_crossing_wave_period'
    'significant_height_of_combined_waves_and_swell'
    'mean_wave_direction'
    'peak_wave_period'
    'mean_wave_period'
    
    """
    
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    if custom_directory == None:
        build_directory('ifs', 
                        'wave')
        
        path = ecmwf_branch_paths('ifs', 
                        'wave')
    else:
        path = custom_branch(custom_directory)
    
    clear_idx_files(path)
    
    url, filename, run = ecmwf_ifs_wave_url_scanner(final_forecast_hour,
                          proxies)

    download = local_file_scanner(path, 
                                  filename,
                                  'ecmwf',
                                  run)
    

    date = parse_filename(filename)
    
    if download == True:
        print(f"Downloading ECMWF IFS Wave...")
        clear_old_data(path)
        for i in range(0, final_forecast_hour + step, step):
            client.get_gridded_data(f"{url}/{date.strftime('%Y%m%d%H')}0000-{i}h-scwv-fc.grib2", 
                        path,
                        f"{date.strftime('%Y%m%d%H')}0000-{i}h-scwv-fc.grib2",
                        proxies=proxies,
                        chunk_size=chunk_size,
                        notifications=notifications)
        
        print(f"ECMWF IFS Wave Download Complete.")
    else:
        print(f"ECMWF IFS Wave Data is up to date. Skipping download...")    
        
        
    if process_data == True:
        print(f"ECMWF IFS Wave Data Processing...")
        
        ds = ecmwf_post_processing.ecmwf_ifs_wave_post_processing(path,
                                                            western_bound, 
                                                            eastern_bound, 
                                                            northern_bound, 
                                                            southern_bound)
        
        clear_idx_files_in_path(path)
        
        print(f"ECMWF IFS Wave Data Processing Complete.")
        return ds
    
    else:
        pass