# Line Query

***def line_query(ds, 
               starting_point,
               ending_point,
               coord_names=['latitude',
                            'longitude'],
               surface_pressure_key='surface_pressure',
               north_to_south=False,
               pressure_level_key='isobaricInhPa'):***

    This function is to query for a line that connects a starting_point (A) with an ending_point (B)
    
    Applications Include
    --------------------
    
    1) Forecast cross-sections between two different geographical points.
    
    Required Arguments:
    
    1) ds (xarray.array) - The forecast model dataset in GRIB format.
    
    2) starting_point (String or Tuple) - The starting point of the line.
    
       The user has two options, either enter an ASOS station identifier as a string OR custom (lat, lon) in decimal degrees as a tuple. 
 
    3) ending_point (String or Tuple) - The ending point of the line.
    
       The user has two options, either enter an ASOS station identifier as a string OR custom (lat, lon) in decimal degrees as a tuple.    
       
    Optional Arguments:
    
    1) coord_names (String List) - Default=['latitude', 'longitude'] A list of the coordinate names (i.e. 'longitude/latitude', 'lon'/'lat', 'easting'/'northing')
    
    2) surface_pressure_key (String) - Default='surface_pressure'. The variable key for surface pressure. 
    
    3) north_to_south (Boolean) - Default=False. When set to False, lines will better reflect a more E to W oriented cross section.
       When True, lines will better reflect a more N to S oriented cross section.
       
    4) pressure_level_key (String) - Default='isobaricInhPa'. The key for the pressure level. 
    
    
    Returns
    -------
    
    5 xarray.array data arrays of pixels along a line between points A and B.
    
    1) ds_grid - The gridded variables. 
    
    2) pressure - The array of pressure levels.
    
    3) index - The indexed point number for each point along the line.
    
    4) lon - Array of longitude.
    
    5) height - Array of height levels.     
