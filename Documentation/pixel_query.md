# Pixel Query

***def pixel_query(ds, 
                latitude=None, 
                longitude=None,
                station_id=None,
                coord_names=['latitude',
                            'longitude']):***

    This function queries for the nearest pixel to a user specified point of (latitude/longitude). 
    
    This function is useful for people interested in a point forecast.
    
    Applications include
    ---------------------
    
    1) forecast soundings
    
    2) forecast meteograms
    
    3) forecast time cross-sections
    
    Required Arguments:
    
    1) ds (xarray.array) - The forecast model dataset in GRIB format. 
    
    Optional Arguments:
    
    1) station_id (String) - Default=None. The 4 letter station ID of an ASOS station.
    
    2) latitude (Float) - Default=None. The latitude of the point in decimal degrees.
    
    3) longitude (Float) - Default=None. The longitude of the point in decimal degrees.
    
    4) coord_names (String List) - Default=['latitude', 'longitude'] A list of the coordinate names (i.e. 'longitude/latitude', 'lon'/'lat', 'easting'/'northing')
    
    Returns
    -------
    
    An xarray.array for the pixel closest to the user specified coordinates or ASOS station.   
