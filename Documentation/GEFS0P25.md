# Global Ensemble Forecast System 0.25 X 0.25 DEGREE (GEFS0P25)

***def gfs_0p25(final_forecast_hour=384, 
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
            convert_temperature=True,
            convert_to='celsius',
            chunk_size=8192,
            notifications='off'):***

This function downloads GFS0P25 data and saves it to a folder. 

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

   **Variables**
   
        'best lifted index'
        'absolute vorticity'
        'convective precipitation'
        'albedo'
        'total precipitation'
        'convective available potential energy'
        'categorical freezing rain'
        'categorical ice pellets'
        'convective inhibition'
        'cloud mixing ratio'
        'plant canopy surface water'
        'percent frozen precipitaion'
        'convective precipitation rate'
        'categorical rain'
        'categorical snow'
        'cloud water'
        'cloud work function'
        'downward longwave radiation flux'
        'dew point'
        'downward shortwave radiation flux'
        'vertical velocity (height)'
        'field capacity'
        'surface friction velocity'
        'ground heat flux'
        'graupel'
        'wind gust'
        'high cloud cover'
        'geopotential height'
        'haines index'
        'storm relative helicity'
        'planetary boundary layer height'
        'icao standard atmosphere reference height'
        'ice cover'
        'ice growth rate'
        'ice thickness'
        'ice temperature'
        'ice water mixing ratio'
        'land cover'
        'low cloud cover'
        'surface lifted index'
        'latent heat net flux'
        'middle cloud cover'
        'mslp (eta model reduction)'
        'ozone mixing ratio'
        'potential evaporation rate'
        'pressure level from which parcel was lifted'
        'potential temperature'
        'precipitation rate'
        'pressure'
        'mean sea level pressure'
        'precipitable water'
        'composite reflectivity'
        'reflectivity'
        'relative humidity'
        'rain mixing ratio'
        'surface roughness'
        'sensible heat net flux'
        'snow mixing ratio'
        'snow depth'
        'liquid volumetric soil moisture (non-frozen)'
        'volumetric soil moisture content'
        'soil type'
        'specific humidity'
        'sunshine duration'
        'total cloud cover'
        'maximum temperature'
        'minimum temperature'
        'temperature'
        'total ozone'
        'soil temperature'
        'momentum flux (u-component)'
        'u-component of wind'
        'zonal flux of gravity wave stress'
        'upward longwave radiation flux'
        'u-component of storm motion'
        'upward shortwave radiation flux'
        'vegetation'
        'momentum flux (v-component)'
        'v-component of wind'
        'meridional flux of gravity wave stress'
        'visibility'
        'ventilation rate'
        'v-component of storm motion'
        'vertical velocity (pressure)'
        'vertical speed shear'
        'water runoff'
        'water equivalent of accumulated snow depth'
        'wilting point'          

11) custom_directory (String or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
    the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
    be used. 

12) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
    of the program you are calling WxData. This setting is to help preserve memory on the machine. 
    
13) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
    either Celsius or Fahrenheit. When False, this data remains in Kelvin.
    
14) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
    Set convert_to='fahrenheit' for Fahrenheit. 
    
15) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
    Default = f:ECMWF/IFS/WAVE
    
16) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.

17) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

Returns: An xarray.array dataset of the most recent GFS0P25 run. 

**Post-processed Variable Key List**

    'mslp'
    'mslp_eta_reduction'
    'hybrid_level_cloud_mixing_ratio'
    'hybrid_level_ice_water_mixing_ratio'
    'hybrid_level_rain_mixing_ratio'
    'hybrid_level_snow_mixing_ratio'
    'hybrid_level_graupel'
    'hybrid_level_derived_radar_reflectivity'
    'boundary_layer_wind_u_component'
    'boundary_layer_wind_v_component'
    'ventilation_rate'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'specific_humidity'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'u_wind_component'
    'v_wind_component'
    'absolute_vorticity'
    'ozone_mixing_ratio'
    'total_cloud_cover'
    'ice_water_mixing_ratio'
    'rain_mixing_ratio'
    'cloud_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'derived_radar_reflectivity'
    '2m_temperature'
    '2m_specific_humidity'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'low_level_u_wind_component'
    'low_level_v_wind_component'
    'low_level_temperature'
    'low_level_specific_humidity'
    'pressure_height_above_ground'
    '100m_u_wind_component'
    '100m_v_wind_component'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    'liquid_volumetric_soil_moisture_non_frozen'
    'temperature_height_above_sea'
    'u_wind_component_height_above_sea'
    'v_wind_component_height_above_sea'
    'precipitable_water'
    'cloud_water'
    'entire_atmosphere_relative_humidity'
    'total_ozone'
    'low_cloud_cover'
    'middle_cloud_cover'
    'high_cloud_cover'
    'cloud_ceiling_height'
    'storm_relative_helicity'
    'u_component_of_storm_motion'
    'v_component_of_storm_motion'
    'tropopause_pressure'
    'tropopause_standard_atmosphere_reference_height'
    'tropopause_height'
    'tropopause_u_wind_component'
    'tropopause_v_wind_component'
    'tropopause_temperature'
    'tropopause_vertical_speed_shear'
    'max_wind_u_component'
    'max_wind_v_component'
    'zero_deg_c_isotherm_geopotential_height'
    'zero_deg_c_isotherm_relative_humidity'
    'highest_tropospheric_freezing_level_geopotential_height'
    'highest_tropospheric_freezing_level_relative_humidity'
    'mixed_layer_temperature'
    'mixed_layer_relative_humidity'
    'mixed_layer_specific_humidity'
    'mixed_layer_u_wind_component'
    'mixed_layer_v_wind_component'
    'mixed_layer_cape'
    'mixed_layer_cin'
    'pressure_level_from_which_a_parcel_was_lifted'
    'sigma_layer_relative_humidity'
    '995_sigma_temperature'
    '995_sigma_theta'
    '995_sigma_relative_humdity'
    '995_u_wind_component'
    '995_v_wind_component'
    '995_vertical_velocity'
    'potential_vorticity_level_u_wind_component'
    'potential_vorticity_level_v_wind_component'
    'potential_vorticity_level_temperature'
    'potential_vorticity_level_geopotential_height'
    'potential_vorticity_level_air_pressure'
    'potential_vorticity_level_vertical_speed_shear' 
