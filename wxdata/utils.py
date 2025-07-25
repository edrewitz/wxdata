import numpy as np
import os

from cartopy.util import add_cyclic_point

def ens_folders(model, cat, ens_members):
    
    """
    This function builds the directories for ensemble members
    """

    if os.path.exists(f"{model}"):
        pass
    else:
        os.mkdir(f"{model}")

    if os.path.exists(f"{model}/{cat}"):
        pass
    else:
        os.mkdir(f"{model}/{cat}")

    paths = []
    for i in range(1, ens_members + 1, 1):
        if os.path.exists(f"{model}/{cat}/{i}"):
            pass
        else:
            os.mkdir(f"{model}/{cat}/{i}")

        path = f"{model}/{cat}/{i}"

        paths.append(path)

    return paths

def shift_longitude(ds, lon_name='longitude'):
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

def lon_bounds(western_bound, eastern_bound):
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

def cyclic_point(ds, parameter, lon_name='longitude'):

    var = ds[parameter]
    var_lon = var[lon_name]
    var_lon_idx = var.dims.index(lon_name)
    var, lon = add_cyclic_point(var.values, coord=var_lon, axis=var_lon_idx)

    return var, lon

def get_u_and_v(wind_speed, wind_dir):

    """
    This function calculates the u and u wind components

    Required Arguments:

    1) wind_speed (Float or Integer) 

    2) wind_direction (Float or Integer)

    Returns
    -------

    u and v wind components
    """

    u = wind_speed * np.cos(wind_dir)
    v = wind_speed * np.sin(wind_dir)

    return u, v

def saturation_vapor_pressure(temperature):

    """
    This function calculates the saturation vapor pressure from temperature.
    This function uses the formula from Bolton 1980.   

    Required Arguments:

    1) temperature (Float or Integer)

    Returns
    -------

    The saturation vapor pressure
    """

    e = 6.112 * np.exp(17.67 * (temperature) / (temperature + 243.5))
    return e


def relative_humidity(temperature, dewpoint):

    """
    This function calculates the relative humidity from temperature and dewpoint. 

    Required Arguments:

    1) temperature (Float or Integer)

    2) dewpoint (Float or Integer)

    Returns
    -------

    The relative humidity
    """

    e = saturation_vapor_pressure(dewpoint)
    e_s = saturation_vapor_pressure(temperature)
    return (e / e_s) * 100
