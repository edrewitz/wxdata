# ECMWF AIFS Post-Processing

***def ecmwf_aifs_post_processing(path,
                            western_bound, 
                            eastern_bound, 
                            northern_bound, 
                            southern_bound):***

    This function does the following:
    
    1) Subsets the ECMWF AIFS model data. 
    
    2) Post-processes the GRIB variable keys into Plain Language variable keys.
    
    Required Arguments:
    
    1) path (String) - The path to the folder containing the ECMWF AIFS files. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray data array of ECMWF data.    
    
    Plain Language ECMWF AIFS Variable Keys 
    ---------------------------------------
    
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
