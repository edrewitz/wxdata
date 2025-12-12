## AIGEFS Single Post-Processing

***def aigefs_single_post_processing(path,
                                   western_bound,
                                   eastern_bound,
                                   northern_bound,
                                   southern_bound):***

    This function post-processes the AIGEFS Data into a more user-friendly format.
    
    Required Arguments:
    
    1) path (String) - The path to the AIGEFS Data files.
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray.array in a plain language variable key format.     
    
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
