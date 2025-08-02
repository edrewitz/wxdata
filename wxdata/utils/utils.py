import os
import gzip

from cartopy.util import add_cyclic_point


def extract_gzipped_file(compressed_file, decompressed_file):
    
    """
    Extracts a gzipped file to a specified location.

    Parameters:
    compressed_file (str): Path to the gzipped file.
    decompressed_file (str): Path where the decompressed file will be saved.
    """

    with gzip.open(compressed_file, 'rb') as f_in:
        with open(decompressed_file, 'wb') as f_out:
            f_out.write(f_in.read())
            
    if os.path.exists(compressed_file):
        os.remove(compressed_file)
    else:
        pass


def clear_idx_files(step=None, model=None, cat=None, paths=None, ens=False):

    """
    This function clears all the .IDX files in a folder.
    """
    
    if ens == False:
        try:
            for item in os.listdir(f"{model}/{cat}/{step}"):
                if item.endswith(".idx"):
                    os.remove(f"{model}/{cat}/{step}/{item}")
        except Exception as e:
            pass
            
    else:
        try:
            for p in paths:
                for item in os.listdir(f"{p}"):
                    if item.endswith(".idx"):
                        os.remove(f"{paths[p]}/{item}")
        except Exception as e:
            pass
        

def ens_folders(model, cat, step, ens_members):
    
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

    if os.path.exists(f"{model}/{cat}/{step}"):
        pass
    else:
        os.mkdir(f"{model}/{cat}/{step}")

    paths = []
    for i in range(1, ens_members + 1, 1):
        if os.path.exists(f"{model}/{cat}/{step}/{i}"):
            pass
        else:
            os.mkdir(f"{model}/{cat}/{step}/{i}")

        path = f"{model}/{cat}/{step}/{i}"

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

