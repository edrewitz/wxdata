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
import warnings
warnings.filterwarnings('ignore')

from wxdata.preprocess.paths import get_branch_path
from wxdata.preprocess.conventions import standardize_var_keys
from wxdata.utils.coords import shift_longitude

sys.tracebacklimit = 0
logging.disable()

def process_data(model, cat, step, directory, western_bound, eastern_bound, northern_bound, southern_bound, ensemble):
    
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
    directory = directory.upper()

    if model == 'GEFS0P50':
    
        ds_list_1 = []
        paths = get_branch_path(model, cat, step, directory)
        
        if ensemble == True:
            for path in paths:

                file_pattern = f"{path}/*.grib2"
                ds1 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'surface'})
                ds1 = shift_longitude(ds1)
                ds1 = ds1.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_1.append(ds1)

            ds_list_2 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds2 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'meanSea'})
                ds2 = shift_longitude(ds2)
                ds2 = ds2.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_2.append(ds2)

            ds_list_3 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds3 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'depthBelowLandLayer'})
                ds3 = shift_longitude(ds3)
                ds3 = ds3.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_3.append(ds3)

            ds_list_4 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds4 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround'})
                ds4 = shift_longitude(ds4)
                ds4 = ds4.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_4.append(ds4)

            ds_list_5 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds5 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'atmosphereSingleLayer'})
                ds5 = shift_longitude(ds5)
                ds5 = ds5.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_5.append(ds5)

            ds_list_6 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds6 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'})
                ds6 = shift_longitude(ds6)
                ds6 = ds6.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_6.append(ds6)

            ds_list_7 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds7 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
                ds7 = shift_longitude(ds7)
                ds7 = ds7.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_7.append(ds7)

            ds_list_8 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds8 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'t'})
                ds8 = shift_longitude(ds8)
                ds8 = ds8.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_8.append(ds8)

            ds_list_9 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds9 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'r'})
                ds9 = shift_longitude(ds9)
                ds9 = ds9.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_9.append(ds9)

            ds_list_10 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds10 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'u'})
                ds10 = shift_longitude(ds10)
                ds10 = ds10.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_10.append(ds10)

            ds_list_11 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds11 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'v'})
                ds11 = shift_longitude(ds11)
                ds11 = ds11.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_11.append(ds11)
                        
                    
                ds_list = []
                ds_list.append(ds_list_1)
                ds_list.append(ds_list_2)
                ds_list.append(ds_list_3)
                ds_list.append(ds_list_4)
                ds_list.append(ds_list_5)
                ds_list.append(ds_list_6)
                ds_list.append(ds_list_7)
                ds_list.append(ds_list_8)
                ds_list.append(ds_list_9)
                ds_list.append(ds_list_10)
                ds_list.append(ds_list_11)     
            
            
                ds = xr.concat(ds_list_1, dim='number')
                ds1 = xr.concat(ds_list_2, dim='number')
                ds2 = xr.concat(ds_list_3, dim='number')
                ds3 = xr.concat(ds_list_4, dim='number')
                ds4 = xr.concat(ds_list_5, dim='number')
                ds5 = xr.concat(ds_list_6, dim='number')
                ds6 = xr.concat(ds_list_7, dim='number')
                ds7 = xr.concat(ds_list_8, dim='number')
                ds8 = xr.concat(ds_list_9, dim='number')
                ds9 = xr.concat(ds_list_10, dim='number')
                ds10 = xr.concat(ds_list_11, dim='number') 
                
                ds['prmsl'] = ds1['prmsl'][:, :, :, :]
                ds['st'] = ds2['st'][:, :, :, :]
                ds['soilw'] = ds2['soilw'][:, :, :, :]
                ds['t2m'] = ds3['t2m'][:, :, :, :]
                ds['r2'] = ds3['r2'][:, :, :, :]
                ds['tmax'] = ds3['tmax'][:, :, :, :]
                ds['tmin'] = ds3['tmin'][:, :, :, :]
                ds['pwat'] = ds4['pwat'][:, :, :, :]
                ds['cape'] = ds5['cape'][:, :, :, :]
                ds['cin'] = ds5['cin'][:, :, :, :]
                ds['gh'] = ds6['gh'][:, :, :, :, :]
                ds['t'] = ds7['t'][:, :, :, :, :]
                ds['r'] = ds8['r'][:, :, :, :, :]
                ds['u'] = ds9['u'][:, :, :, :, :]
                ds['v'] = ds10['v'][:, :, :, :, :]
            
        else:

            path = paths
            
            file_pattern = f"{path}/*.grib2"
            
            ds = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'surface'})
            ds = shift_longitude(ds)
            ds = ds.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            ds1 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'meanSea'})
            ds1 = shift_longitude(ds1)
            ds1 = ds1.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            ds2 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'depthBelowLandLayer'})
            ds2 = shift_longitude(ds2)
            ds2 = ds2.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            ds3 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround'})
            ds3 = shift_longitude(ds3)
            ds3 = ds3.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            ds4 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'atmosphereSingleLayer'})
            ds4 = shift_longitude(ds4)
            ds4 = ds4.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            ds5 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'})
            ds5 = shift_longitude(ds5)
            ds5 = ds5.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            ds6 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
            ds6 = shift_longitude(ds6)
            ds6 = ds6.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            ds7 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'t'})
            ds7 = shift_longitude(ds7)
            ds7 = ds7.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            ds8 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'r'})
            ds8 = shift_longitude(ds8)
            ds8 = ds8.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            ds9 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'u'})
            ds9 = shift_longitude(ds9)
            ds9 = ds9.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            ds10 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'v'})
            ds10 = shift_longitude(ds10)
            ds10 = ds10.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            ds
            
            ds['prmsl'] = ds1['prmsl'][:, :, :]
            ds['st'] = ds2['st'][:, :, :]
            ds['soilw'] = ds2['soilw'][:, :, :]
            ds['t2m'] = ds3['t2m'][:, :, :]
            ds['r2'] = ds3['r2'][:, :, :]
            ds['tmax'] = ds3['tmax'][:, :, :]
            ds['tmin'] = ds3['tmin'][:, :, :]
            ds['pwat'] = ds4['pwat'][:, :, :]
            ds['cape'] = ds5['cape'][:, :, :]
            ds['cin'] = ds5['cin'][:, :, :]
            ds['gh'] = ds6['gh'][:, :, :, :]
            ds['t'] = ds7['t'][:, :, :, :]
            ds['r'] = ds8['r'][:, :, :, :]
            ds['u'] = ds9['u'][:, :, :, :]
            ds['v'] = ds10['v'][:, :, :, :]
            
        ds = standardize_var_keys(ds, model)        
    
    return ds