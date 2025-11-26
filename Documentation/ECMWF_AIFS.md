# ECMWF AIFS

***def ecmwf_aifs(final_forecast_hour=360,
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
              notifications='off'):***

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
