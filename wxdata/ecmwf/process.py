"""
This file hosts the function responsible for ECMWF data post-processing. 

GRIB variable keys will be post-processed into Plain Language variable keys. 

(C) Eric J. Drewitz 2025
"""
import xarray as xr
import glob
import sys
import logging
import numpy as np
import metpy.calc as mpcalc
import warnings
warnings.filterwarnings('ignore')

from wxdata.ecmwf.paths import(
    ecmwf_branch_paths,
    sorted_paths
)

from wxdata.calc.thermodynamics import relative_humidity

sys.tracebacklimit = 0
logging.disable()

def process_ecmwf_ifs_data(western_bound, 
                           eastern_bound, 
                           northern_bound, 
                           southern_bound):
    
    """
    This function does the following:
    
    1) Subsets the ECMWF IFS model data. 
    
    2) Post-processes the GRIB variable keys into Plain Language variable keys.
    
    Required Arguments:
    
    1) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    2) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    3) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    4) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray data array of ECMWF data.    
    
    Plain Language Variable Keys 
    ----------------------------
    
    'total_column_water'
    'total_column_vertically_integrated_water_vapor'
    'snow_albedo'
    'land_sea_mask'
    'specific_humidity'
    'volumetric_soil_moisture_content'
    'sea_ice_thickness'
    'soil_temperature'
    'surface_longwave_radiation_downward'
    'surface_net_shortwave_solar_radiation'
    'surface_net_longwave_thermal_radiation'
    'top_net_longwave_thermal_radiation'
    '10m_max_wind_gust'
    'vertical_velocity'
    'relative_vorticity'
    'relative_humidity'
    'geopotential_height'
    'eastward_turbulent_surface_stress'
    'u_wind_component'
    'divergence'
    'northward_turbulent_surface_stress'
    'v_wind_component'
    'air_temperature'
    'water_runoff'
    'total_precipitation'
    'mslp'
    'eastward_surface_sea_water_velocity'
    'most_unstable_cape'
    'northward_surface_sea_water_velocity'
    'sea_surface_height'
    'standard_deviation_of_sub_gridscale_orography'
    'skin_temperature'
    'slope_of_sub_gridscale_orography'
    '10m_u_wind_component'
    'precipitation_type'
    '10m_v_wind_component'
    'total_precipitation_rate'
    'surface_shortwave_radiation_downward'
    'geopotential'
    'surface_pressure'
    '2m_temperature'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    'absolute_vortcity'
    'curvature_vorticity'
    'dew_point'
    'temperature_advection'
    'vorticity_advection'
    'humidity_advection'
    'potential_temperature'
    'mixing_ratio'
    'dry_lapse_rate'


     
    """
    
    path = ecmwf_branch_paths('ifs',
                              'operational')
    
    files = sorted_paths(path)
    
    try:
        ds = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
    except Exception as e:
        pass
    
    try:
        ds1 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False, 
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':238167}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                        latitude=slice(northern_bound, southern_bound, 1))
    
    except Exception as e:
        pass
    
    try:
        ds2 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':228246}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                       latitude=slice(northern_bound, southern_bound, 1))
    
    except Exception as e:
        pass
    
    try:
        ds3 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':228247}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                       latitude=slice(northern_bound, southern_bound, 1))
        
    except Exception as e:
        pass
    
    try:
        ds4 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':168}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                    latitude=slice(northern_bound, southern_bound, 1))
    except Exception as e:
        pass
    
    try:
        ds = ds.drop_duplicates(dim="step", keep="first")
    except Exception as e:
        pass
    
    try:
        ds1 = ds1.drop_duplicates(dim="step", keep="first")
    except Exception as e:
        pass
    
    try:
        ds2 = ds2.drop_duplicates(dim="step", keep="first")
    except Exception as e:
        pass
        
    try:
        ds3 = ds3.drop_duplicates(dim="step", keep="first")
    except Exception as e:
        pass
    
    try:
        ds4 = ds4.drop_duplicates(dim="step", keep="first")
    except Exception as e:
        pass
    
    try:
        ds['total_column_water'] = ds['tcw']
        ds = ds.drop_vars('tcw')
    except Exception as e:
        pass
    
    try:
        ds['total_column_vertically_integrated_water_vapor'] = ds['tcwv']
        ds = ds.drop_vars('tcwv')
    except Exception as e:
        pass
    
    try:
        ds['snow_albedo'] = ds['asn']
        ds = ds.drop_vars('asn')
    except Exception as e:
        pass
    
    try:
        ds['land_sea_mask'] = ds['lsm']
        ds = ds.drop_vars('lsm')
    except Exception as e:
        pass
    
    try:
        ds['specific_humidity'] = ds['q']
        ds = ds.drop_vars('q')
    except Exception as e:
        pass
    
    try:
        ds['volumetric_soil_moisture_content'] = ds['vsw']
        ds = ds.drop_vars('vsw')
    except Exception as e:
        pass
    
    try:
        ds['precipitable_water'] = ds['tcvw']
        ds = ds.drop_vars('tcvw')
    except Exception as e:
        pass
    
    try:     
        ds['sea_ice_thickness'] = ds['sithick']
        ds = ds.drop_vars('sithick')
    except Exception as e:
        pass     
    
    try:
        ds['soil_temperature'] = ds['sot']
        ds = ds.drop_vars('sot')
    except Exception as e:
        pass
    
    try:
        ds['surface_longwave_radiation_downward'] = ds['strd']
        ds = ds.drop_vars('strd')
    except Exception as e:
        pass
    
    try:
        ds['surface_net_shortwave_solar_radiation'] = ds['ssr']
        ds = ds.drop_vars('ssr')
    except Exception as e:
        pass
    
    try:
        ds['surface_net_longwave_thermal_radiation'] = ds['str']
        ds = ds.drop_vars('str')
    except Exception as e:
        pass
    
    try:
        ds['top_net_longwave_thermal_radiation'] = ds['ttr']
        ds = ds.drop_vars('ttr')
    except Exception as e:
        pass
    
    try:
        ds['10m_max_wind_gust'] = ds['max_i10fg']
        ds = ds.drop_vars('max_i10fg')
    except Exception as e:
        pass
    
    try:
        ds['vertical_velocity'] = ds['w']
        ds = ds.drop_vars('w')
    except Exception as e:
        pass
    
    try:
        ds['relative_vorticity'] = ds['vo']
        ds = ds.drop_vars('vo')
    except Exception as e:
        pass
    
    try:
        ds['relative_humidity'] = ds['r']
        ds = ds.drop_vars('r')
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height'] = ds['gh']
        ds = ds.drop_vars('gh')
    except Exception as e:
        pass
    
    try:
        ds['eastward_turbulent_surface_stress'] = ds['ewss']
        ds = ds.drop_vars('ewss')
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component'] = ds['u']
        ds = ds.drop('u')
    except Exception as e:
        pass
    
    try:
        ds['divergence'] = ds['d']
        ds = ds.drop_vars('d')
    except Exception as e:
        pass
    
    try:
        ds['northward_turbulent_surface_stress'] = ds['nsss']
        ds = ds.drop_vars('nsss')
    except Exception as e:
        pass
    
    try:
        ds['v_wind_component'] = ds['v']
        ds = ds.drop_vars('v')
    except Exception as e:
        pass
    
    try:
        ds['wind_speed'] = mpcalc.wind_speed(ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['wind_direction'] = mpcalc.wind_direction(ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['air_temperature'] = ds['t']
        ds = ds.drop_vars('t')
    except Exception as e:
        pass
    
    try:
        ds['water_runoff'] = ds['ro']
        ds = ds.drop_vars('ro')
    except Exception as e:
        pass
    
    try:
        ds['total_precipitation'] = ds['tp']
        ds = ds.drop_vars('tp')
    except Exception as e:
        pass
    
    try:
        ds['mslp'] = ds['msl']
        ds = ds.drop_vars('msl')
    except Exception as e:
        pass
    
    try:
        ds['eastward_surface_sea_water_velocity'] = ds['sve']
        ds = ds.drop_vars('sve')
    except Exception as e:
        pass
    
    try:
        ds['most_unstable_cape'] = ds['mucape']
        ds = ds.drop_vars('mucape')
    except Exception as e:
        pass
    
    try:
        ds['northward_surface_sea_water_velocity'] = ds['svn']
        ds = ds.drop_vars('svn')
    except Exception as e:
        pass
    
    try:
        ds['sea_surface_height'] = ds['zos']
        ds = ds.drop_vars('zos')
    except Exception as e:
        pass
    
    try:
        ds['standard_deviation_of_sub_gridscale_orography'] = ds['sdor']
        ds = ds.drop_vars('sdor')
    except Exception as e:
        pass
    
    try:
        ds['skin_temperature'] = ds['skt']
        ds = ds.drop_vars('skt')
    except Exception as e:
        pass
    
    try:
        ds['slope_of_sub_gridscale_orography'] = ds['slor']
        ds = ds.drop_vars('slor')
    except Exception as e:
        pass
    
    try:
        ds['10m_u_wind_component'] = ds['u10']
        ds = ds.drop_vars('u10')
    except Exception as e:
        pass
    
    try:
        ds['precipitation_type'] = ds['ptype']
        ds = ds.drop_vars('ptype')
    except Exception as e:
        pass
    
    try:
        ds['10m_v_wind_component'] = ds['v10']
        ds = ds.drop_vars('v10')
    except Exception as e:
        pass
    
    try:
        ds['total_precipitation_rate'] = ds['tprate']
        ds = ds.drop_vars('tprate')
    except Exception as e:
        pass
    
    try:
        ds['surface_shortwave_radiation_downward'] = ds['ssrd']
        ds = ds.drop_vars('ssrd')
    except Exception as e:
        pass
    
    try:
        ds['geopotential'] = ds['z']
        ds = ds.drop_vars('z')
    except Exception as e:
        pass
    
    try:
        ds['surface_pressure'] = ds['sp']
        ds = ds.drop_vars('sp')
    except Exception as e:
        pass
    
    try:
        ds['2m_temperature'] = ds1['t2m']
    except Exception as e:
        pass
    
    try:
        ds['100m_u_wind_component'] = ds2['u100']
    except Exception as e:
        pass
    
    try:
        ds['100m_v_wind_component'] = ds3['v100']
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point'] = ds4['d2m']
    except Exception as e:
        pass
    
    try:
        ds['2m_relative_humidity'] = relative_humidity(ds['2m_temperature'],
                                                       ds['2m_dew_point'])
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point_depression'] = ds['2m_temperature'] - ds['2m_dew_point']
    except Exception as e:
        pass
    
    try:
        ds['absolute_vortcity'] = mpcalc.absolute_vorticity(ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['absolute_momentum'] = mpcalc.absolute_momentum(ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['ageostrophic_wind'] = mpcalc.ageostrophic_wind(ds['geopotential_height'], ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['curvature_vorticity'] = mpcalc.curvature_vorticity(ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['divergence'] = mpcalc.divergence(ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['geostrophic_wind'] = mpcalc.geostrophic_wind(ds['geopotential_height'])
    except Exception as e:
        pass
    
    try:
        ds['dew_point'] = mpcalc.dewpoint_from_relative_humidity(ds['air_temperature'], ds['relative_humidity'])
    except Exception as e:
        pass
    
    try:
        ds['dew_point_depression'] = ds['air_temperature'] - ds['dew_point']
    except Exception as e:
        pass
    
    try:
        ds['temperature_advection'] = mpcalc.advection(ds['air_temperature'], u=ds['u_wind_component'], v=ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['vorticity_advection'] = mpcalc.advection(ds['absolute_vortcity'], u=ds['u_wind_component'], v=ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['precipitable_water_advection'] = mpcalc.advection(ds['precipitable_water'], u=ds['u_wind_component'], v=ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['humidity_advection'] = mpcalc.advection(ds['relative_humidity'], u=ds['u_wind_component'], v=ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['potential_temperature'] = mpcalc.potential_temperature(ds['isobaricInhPa'], ds['air_temperature'])
    except Exception as e:
        pass
    
    try:
        ds['frontogenesis'] = mpcalc.frontogenesis(ds['potential_temperature'], ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['mixing_ratio'] = mpcalc.mixing_ratio_from_relative_humidity(ds['isobaricInhPa'], ds['air_temperature'], ds['relative_humidity'])
    except Exception as e:
        pass
    
    try:
        ds['moist_lapse_rate'] = mpcalc.moist_lapse(ds['isobaricInhPa'], ds['air_temperature'])
    except Exception as e:
        pass
    
    try:
        ds['dry_lapse_rate'] = mpcalc.dry_lapse(ds['isobaricInhPa'], ds['air_temperature'])
    except Exception as e:
        pass
    
    try:
        ds['showalter_index'] = mpcalc.showalter_index(ds['isobaricInhPa'], ds['air_temperature'], ds['dew_point'])
    except Exception as e:
        pass
    
    try:
        ds['bulk_shear'] = mpcalc.bulk_shear(ds['isobaricInhPa'], ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
        
        
    ds = ds.metpy.dequantify()
    return ds