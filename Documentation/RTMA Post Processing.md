# Real Time Mesoscale Analysis (RTMA) Post-Processing

***def process_rtma_data(filename, 
                     model,
                     directory):***

    This function post-processes RTMA Data and returns an xarray data array of the data.
    
    This post-processing will convert all variable names into a plain language format. 
    
    
    Required Arguments: 
    
    1) path (String) - The path to the file that has the RTMA Data. 
    
    2) model (String) - Default='rtma'. The RTMA model being used:
    
    RTMA Models
    -----------
    
    CONUS = 'rtma'
    Alaska = 'ak rtma'
    Hawaii = 'hi rtma'
    Puerto Rico = 'pr rtma'
    Guam = 'gu rtma'
    
    3) directory (String) - The directory path where the RTMA files are saved to. 
    
    Optional Arguments: None
    
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
