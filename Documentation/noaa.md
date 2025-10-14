# NOAA: Get Storm Prediction Center Outlooks And National Weather Service Forecasts (NDFD Grids)

***def get_ndfd_grids(parameter, 
                   state,
                   clear_recycle_bin=True):***

This function retrieves the latest NWS Forecast (NDFD) files from the NWS FTP Server. 

Data Source: NOAA/NWS/NDFD (tgftp.nws.noaa.gov)

Required Arguments: 

1) parameter (String) - The parameter that the user wishes to download.

          Parameters
          
          'maximum_relative_humidity'
          'mainimum_relative_humidity'
          'maximum_temperature'
          'minimum_temperature'
          'relative_humidity'
          'temperature'
          'apparent_temperature'
          'wind_speed'
          'wind_gust'
          'wind_direction'
          'spc_critical_fire_weather_forecast'
          'spc_dry_lightning_forecast'
          'spc_convective_outlook'
          'ice_accumulation'
          'probability_of_hail'
          '12_hour_probability_of_precipitation'
          'probability_of_extreme_tornadoes'
          'total_probability_of_severe_thunderstorms'
          'total_probability_of_extreme_severe_thunderstorms'
          'probability_of_extreme_thunderstorm_winds'
          'probability_of_extreme_hail'
          'probability_of_extreme_tornadoes'
          'probability_of_damaging_thunderstorm_winds'
          'quantitative_precipitation_forecast'
          'sky_cover'
          'snow_amount'
          'snow_level'
          'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_cumulative'
          'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_incremental'
          'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_cumulative'
          'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_incremental'
          'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_cumulative'
          'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_incremental'
          'dew_point'
          'visibility'
          'significant_wave_height'
          'warnings'
          'weather'  

2) state (String) - The state or region being used. 

Optional Arguments: 

1) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
    of the program you are calling WxData. This setting is to help preserve memory on the machine. 

Returns
-------

An xarray.data array of the latest NWS/SPC Forecast data.

Variable names are also changed from their origional key value into plain language.
    
        Plain Language Variable Key List
        
        'maximum_relative_humidity'
        'mainimum_relative_humidity'
        'maximum_temperature'
        'minimum_temperature'
        'relative_humidity'
        'temperature'
        'apparent_temperature'
        'wind_speed'
        'wind_gust'
        'wind_direction'
        'spc_critical_fire_weather_forecast'
        'spc_dry_lightning_forecast'
        'spc_convective_outlook'
        'ice_accumulation'
        'probability_of_hail'
        '12_hour_probability_of_precipitation'
        'probability_of_extreme_tornadoes'
        'total_probability_of_severe_thunderstorms'
        'total_probability_of_extreme_severe_thunderstorms'
        'probability_of_extreme_thunderstorm_winds'
        'probability_of_extreme_hail'
        'probability_of_extreme_tornadoes'
        'probability_of_damaging_thunderstorm_winds'
        'quantitative_precipitation_forecast'
        'sky_cover'
        'snow_amount'
        'snow_level'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_cumulative'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_incremental'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_cumulative'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_incremental'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_cumulative'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_incremental'
        'dew_point'
        'visibility'
        'significant_wave_height'
        'warnings'
        'weather'   
