# ECMWF IFS Wave Post-Processing

***def ecmwf_ifs_wave_post_processing(path,
                            western_bound, 
                            eastern_bound, 
                            northern_bound, 
                            southern_bound):***

    This function does the following:
    
    1) Subsets the ECMWF IFS Wave model data. 
    
    2) Post-processes the GRIB variable keys into Plain Language variable keys.
    
    Required Arguments:
    
    1) path (String) - The path to the folder containing the ECMWF IFS Wave files. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray data array of ECMWF data.    
    
    Plain Language ECMWF IFS Wave Variable Keys 
    -------------------------------------------
    
    'mean_zero_crossing_wave_period'
    'significant_height_of_combined_waves_and_swell'
    'mean_wave_direction'
    'peak_wave_period'
    'mean_wave_period'
