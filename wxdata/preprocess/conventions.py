"""
This file hosts the functions that rename all variable keys into a common convention.

(C) Eric J. Drewitz 2025
"""

def standardize_var_keys(ds, model):
    
    """
    This function parses and renames all GEFS0P50 variable keys into a common convention.
    
    Required Arguments:
    
    1) ds (xarray data array) - The dataset.
    
    2) model (String) - The computer model being used.  
    
    Returns
    -------
    
    An updated dataset parsed with a common naming convention    
    """
    
    model = model.upper()
    
    if model == 'GEFS0P50':

        ds['surface_pressure'] = ds['sp']
        ds['orography'] = ds['orog']
        ds['accumulated_snow_depth_swe'] = ds['sdwe']
        ds['snow_depth'] = ds['sde']
        ds['sea_ice_thickness'] = ds['sithick']
        ds['total_precipitation'] = ds['tp']
        ds['categorical_snow'] = ds['csnow']
        ds['categorical_ice_pellets'] = ds['cicep']
        ds['categorical_freezing_rain'] = ds['cfrzr']
        ds['categorical_rain'] = ds['crain']
        ds['time_mean_surface_latent_heat_flux'] = ds['avg_slhtf']
        ds['time_mean_surface_sensible_heat_flux'] = ds['avg_ishf']
        ds['surface_downward_shortwave_radiation_flux'] = ds['sdswrf']
        ds['surface_downward_longwave_radiation_flux'] = ds['sdlwrf']
        ds['surface_upward_shortwave_radiation_flux'] = ds['suswrf']
        ds['surface_upward_longwave_radiation_flux'] = ds['sulwrf']
        ds['mslp'] = ds['prmsl']
        ds['soil_temperature'] = ds['st']
        ds['soil_moisture'] = ds['soilw']
        ds['2m_relative_humidity'] = ds['r2']
        ds['2m_temperature'] = ds['t2m']
        ds['maximum_temperature'] = ds['tmax']
        ds['minimum_temperature'] = ds['tmin']
        ds['precipitable_water'] = ds['pwat']
        ds['geopotential_height'] = ds['gh']
        ds['air_temperature'] = ds['t']
        ds['relative_humidity'] = ds['r']
        ds['u_wind_component'] = ds['u']
        ds['v_wind_component'] = ds['v']
                     
        ds = ds.drop_vars(
            ['sp', 
             'orog', 
             'sdwe',
             'sde',
             'sithick',
             'tp',
             'csnow',
             'cicep',
             'cfrzr',
             'crain',
             'avg_slhtf',
             'avg_ishf',
             'sdswrf',
             'sdlwrf',
             'suswrf',
             'sulwrf',
             'prmsl',
             'st',
             'soilw',
             'r2',
             't2m',
             'tmax',
             'tmin',
             'pwat',
             'gh',
             't',
             'r',
             'u',
             'v']
            )
    
    
    return ds