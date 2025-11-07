"""
This file hosts functions that process geographical coordinates in netCDF data.

(C) Eric J. Drewitz 2025
"""
from cartopy.util import add_cyclic_point

def convert_lon(western_bound, eastern_bound):
    
    """
    This function converts longitude from -180 to 180 to 0 to 360
    
    Required Arguments: 
    
    1) lon (float) - The longitude of a point. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    The longitude in terms of 0 to 360.     
    """
    
    if western_bound < 0 and eastern_bound < 0:
        western_bound = 360 - abs(western_bound)
        eastern_bound = 360 - abs(eastern_bound)

    elif western_bound > 0 and eastern_bound > 0:
        western_bound = western_bound
        eastern_bound = eastern_bound

    else:
        western_bound = (2 * western_bound) + 360
        eastern_bound = 180 + eastern_bound

    return western_bound, eastern_bound

def shift_longitude(ds, 
                    lon_name='longitude'):
    """
    Shifts longitude values to ensure continuity across the Prime Meridian.

    Required Arguments:

    1) ds (xarray.dataarray) - The dataset of the model data.

    Optional Arguments:

    1) lon_name (String) - Default = longitude. The abbreviation for the longitude key.

    Returns
    -------

    An xarray.dataarray with longitude coordinates ranging from -180 to 180
    """
    lon = ds[lon_name].values
    lon_shifted = (lon + 180) % 360 - 180
    ds = ds.assign_coords({lon_name: lon_shifted})
    ds = ds.sortby(lon_name)
    return ds

def lon_bounds(western_bound, 
               eastern_bound):
    """
    This function calculates the western bound with 360 being at the Prime Meridian

    Required Arguments:

    1) western_bound (Float or Integer)
    2) eastern_bound (Float or Integer)

    Returns
    -------

    Western and Eastern Bounds with 0 to 360 coordinates. 
    """
    if western_bound < 0:
        western_bound = abs(western_bound)
    else:
        western_bound = 360 - western_bound

    if eastern_bound < 0:
        eastern_bound = abs(eastern_bound)
    else:
        eastern_bound = 360 - eastern_bound

    return western_bound, eastern_bound

def cyclic_point(ds, 
                 parameter, 
                 lon_name='longitude'):
    
    """
    This function returns a data array for the full 360 degree Earth. 
    
    Required Arguments:
    
    1) ds (xarray data array) - The xarray dataset.
    
    2) parameter (String) - The parameter or variable the user is plotting. 
    
    Optional Arguments:
    
    1) lon_name (String) - The name of the longitude variable. Usually is lon or longitude. 
    
    Returns
    -------
    
    An xarray data array that interpolates along 180 degrees longitude.     
    """

    var = ds[parameter]
    var_lon = var[lon_name]
    var_lon_idx = var.dims.index(lon_name)
    var, lon = add_cyclic_point(var.values, coord=var_lon, axis=var_lon_idx)

    return var, lon
