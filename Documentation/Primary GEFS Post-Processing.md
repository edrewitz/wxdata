# Primary GEFS Variables Post-Processing

***def primary_gefs_post_processing(paths):***

    This function post-processes the GEFS (Primary) Parameters for GEFS0P50 and GEFS0P25. 
    
    Required Arguments: 
    
    1) paths (List) - A list of file paths to the GEFS0P50 or GEFS0P25 files. 
    
    Returns
    -------
    
    An xarray data array of the post-processed GEFS data. 
    GRIB Keys are converted to Plain Language Keys. 
    
    New Variable Keys After Post-Processing (Decrypted GRIB Keys Into Plain Language)
    --------------------------------------------------------------------------------
    
    GEFS0P50
    --------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'mixed_layer_cape'
    'mixed_layer_cin'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'u_wind_component'
    'v_wind_component'
    
    GEFS0P25
    --------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'surface_visibility'
    'surface_wind_gust'
    'percent_frozen_precipitation'
    'surface_cape'
    'surface_cin'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    '2m_dew_point'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'mixed_layer_cape'
    'mixed_layer_cin'
    '3km_helicity'
