# GFS 0.25x0.25 Degree Secondary Parameters

***def gfs_0p25_secondary_parameters(final_forecast_hour=384, 
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
            convert_temperature=True,
            convert_to='celsius',
            chunk_size=8192,
            notifications='off'):***

    This function downloads GFS0P25 SECONDARY PARAMETERS data and saves it to a folder. 
    
    Required Argumemnts: None
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GFS0P25
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 6 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. Set to 3 for 3hr increments and 6 for 6hrly increments.
    
    7) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
       
    9) variables (String List) - The variables the user wishes to query.
    
        Variables
        ---------
        
        'absolute vorticity'
        'clear sky uv-b downward solar flux'
        'cloud mixing ratio'
        'plant canopy surface water'
        'uv-b downward solar flux'
        'vertical velocity (height)'
        'graupel'
        'geopotential height'
        'ice thickness'
        'ice water mixing ratio'
        'ozone mixing ratio'
        'pressure'
        'relative humidity'
        'rain mixing ratio'
        'snow mixing ratio'
        'liquid volumetric soil moisture (non-frozen)'
        'specific humidity'
        'total cloud cover'
        'temperature'
        'u-component of wind'
        'v-component of wind'
        'vertical velocity (pressure)'
        'vertical speed shear'      
    
    10) custom_directory (String or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. 
    
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
    
    An xarray.array dataset of the most recent GFS0P25 run. 
    
    Post-processed Variable Key List
    --------------------------------
    
    'u_wind_component'
    'v_wind_component'
    'air_temperature'
    'relative_humidity'
    'absolute_vorticity'
    'geopotential_height'
    'ozone_mixing_ratio'
    'total_cloud_cover'
    'cloud_mixing_ratio'
    'ice_water_mixing_ratio'
    'rain_water_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'liquid_volumetric_soil_moisture_non_frozen'
    'plant_canopy_surface_water'
    'sea_ice_thickness'
    'temperature_height_above_sea'
    'u_wind_component_height_above_sea'
    'v_wind_component_height_above_sea'
    'mixed_layer_temperature'
    'mixed_layer_relative_humidity'
    'mixed_layer_specific_humidity'
    'mixed_layer_u_wind_component'
    'mixed_layer_v_wind_component'
    'potential_vorticity_level_u_wind_component'
    'potential_vorticity_level_v_wind_component'
    'potential_vorticity_level_temperature'
    'potential_vorticity_level_geopotential_height'
    'potential_vorticity_level_air_pressure'
    'potential_vorticity_level_vertical_speed_shear' 
