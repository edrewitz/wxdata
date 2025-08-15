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
    
        ds['surface_pressure'] = ds['sp'][0, :, :, :]
        ds['orography'] = ds['orog'][0, :, :, :]
        ds['accumulated_snow_depth_swe'] = ds['sdwe'][0, :, :, :]
        ds['snow_depth'] = ds['sde'][0, :, :, :]
        ds['sea_ice_thickness'] = ds['sithick'][0, :, :, :]
        ds['total_precipitation'] = ds['tp'][0, :, :, :]
        ds['categorical_snow'] = ds['csnow'][0, :, :, :]
        ds['categorical_ice_pellets'] = ds['cicep'][0, :, :, :]
        ds['categorical_freezing_rain'] = ds['cfrzr'][0, :, :, :]
        ds['categorical_rain'] = ds['crain'][0, :, :, :]
        ds['time_mean_surface_latent_heat_flux'] = ds['avg_slhtf'][0, :, :, :]
        ds['time_mean_surface_sensible_heat_flux'] = ds['avg_ishf'][0, :, :, :]
        ds['surface_downward_shortwave_radiation_flux'] = ds['sdswrf'][0, :, :, :]
        ds['surface_downward_longwave_radiation_flux'] = ds['sdlwrf'][0, :, :, :]
        ds['surface_upward_shortwave_radiation_flux'] = ds['suswrf'][0, :, :, :]
        ds['surface_upward_longwave_radiation_flux'] = ds['sulwrf'][0, :, :, :]
        ds['mslp'] = ds['prmsl'][1, :, :, :]
        ds['soil_temperature'] = ds['st'][2, :, :, :]
        ds['soil_moisture'] = ds['soilw'][2, :, :, :]
        ds['2m_relative_humidity'] = ds['r2'][3, :, :, :]
        ds['2m_temperature'] = ds['t2m'][3, :, :, :]
        ds['maximum_temperature'] = ds['tmax'][3, :, :, :]
        ds['minimum_temperature'] = ds['tmin'][3, :, :, :]
        ds['precipitable_water'] = ds['pwat'][4, :, :, :]
        ds['cape'] = ds['cape'][5, :, :, :]
        ds['cin'] = ds['cin'][5, :, :, :]
        ds['air_temperature'] = ds['t'][6, :, :, :, :]
        ds['relative_humidity'] = ds['r'][7, :, :, :, :]
        ds['u_wind_component'] = ds['u'][8, :, :, :, :]
        ds['v_wind_component'] = ds['v'][9, :, :, :, :]

    ds.drop_dims('time')
    
    return ds