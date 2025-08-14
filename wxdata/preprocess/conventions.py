"""
This file hosts the functions that rename all variable keys into a common convention.

(C) Eric J. Drewitz 2025
"""

def gefs0p50(ds):
    
    """
    This function parses and renames all GEFS0P50 variable keys into a common convention.
    
    Required Arguments:
    
    1) ds (xarray data array) - The dataset. 
    
    Returns
    -------
    
    An updated dataset parsed with a common naming convention    
    """
    
    ds['surface_pressure'] = ds['sp'][0, :, :, :]
    ds['orography'] = ds['orog'][0, :, :, :]
    ds['accumulated_snow_depth_swe'] = ds['sdwe'][0, :, :, :]
    ds['snow_depth'] = ds['sde'][0, :, :, :]
    ds['sea_ice_thickness'] = ds['sithick'][0, :, :, :]
    ds['mslp'] = ds['prmsl'][1, :, :, :]
    ds['soil_temperature'] = ds['st'][2, :, :, :]
    ds['soil_moisture'] = ds['soilw'][2, :, :, :]
    ds['2m_relative_humidity'] = ds['r2'][3, :, :, :]
    ds['2m_temperature'] = ds['t2m'][3, :, :, :]
    ds['precipitable_water'] = ds['pwat'][4, :, :, :]
    ds['air_temperature'] = ds['t'][6, :, :, :, :]
    ds['relative_humidity'] = ds['r'][7, :, :, :, :]
    
    return ds