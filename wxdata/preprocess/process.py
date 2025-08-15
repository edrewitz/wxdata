"""
This file hosts the functions that pre-process GEFS Data.

Pre-Processing includes the following:

1) Extracting the variables keys for a list of the various 'typeOfLevel'
2) Renaming the variable names in a common notation for users to understand. 
3) Returning an xarray data array of pre-processed data to the user. 

(C) Eric J. Drewitz 2025
"""
import xarray as xr
import glob
import sys
import logging
import numpy as np

from wxdata.preprocess.keys import get_var_keys
from wxdata.preprocess.paths import get_branch_path
from wxdata.preprocess.conventions import standardize_var_keys
from wxdata.utils.coords import shift_longitude

sys.tracebacklimit = 0
logging.disable()

def process_data(model, cat, step, western_bound, eastern_bound, northern_bound, southern_bound, ensemble):
    
    """
    This function pre-processes model. 
    
    Required Arguments:

    1) model (String) - The forecast model. 

    2) cat (String) - cat (String) - The category of the data. (i.e. mean, control, all members).

    3) step (Integer) - The forecast increment. Either 3, 6 or 12 hour increments.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray data array of the pre-processed GEFS0P50 Data.    
    """
    model = model.upper()
    cat = cat.upper()
    
    if ensemble == False:    
        path = get_branch_path(model, cat, step)
        
        keys, short_names = get_var_keys(model)
        
        ds_list = []
        
        file_pattern = f"{path}/*.grib2"
        
        for key in keys:
            
            if key != 'isobaricInhPa':
                ds = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': key})
            
                if np.nanmax(ds['longitude']) > 180:         
                    ds = shift_longitude(ds)
                else:
                    pass
                
                ds = ds.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                
                ds_list.append(ds)
            
            else:
                for name in short_names:
                    ds = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': key, 'shortName': name})
            
                    if np.nanmax(ds['longitude']) > 180:         
                        ds = shift_longitude(ds)
                    else:
                        pass
                    
                    ds = ds.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                    
                    ds_list.append(ds)  
                              
        ds = xr.concat(ds_list, dim='time')
        ds = standardize_var_keys(ds, model)
    
    return ds