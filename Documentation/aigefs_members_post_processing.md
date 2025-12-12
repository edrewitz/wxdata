## AIGEFS Members Post-Processing

***def aigefs_members_post_processing(paths,
                                   western_bound,
                                   eastern_bound,
                                   northern_bound,
                                   southern_bound):***

    This function post-processes the AIGEFS Data into a more user-friendly format.
    
    Required Arguments:
    
    1) paths (String List) - The list of the paths to the AIGEFS Data files.
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray.array in a plain language variable key format.   
