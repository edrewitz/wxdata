"""
This file hosts the function responsible for ECMWF data post-processing. 

GRIB variable keys will be post-processed into Plain Language variable keys. 

(C) Eric J. Drewitz 2025
"""
import xarray as xr
import sys
import logging
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from wxdata.calc.thermodynamics import relative_humidity
from wxdata.utils.file_funcs import(
    clear_idx_files_in_path,
    sorted_paths
)

sys.tracebacklimit = 0
logging.disable()

def ecmwf_ifs_post_processing(path,
                            western_bound, 
                            eastern_bound, 
                            northern_bound, 
                            southern_bound):
    
    """
    This function does the following:
    
    1) Subsets the ECMWF IFS and High Resolution IFS model data. 
    
    2) Post-processes the GRIB variable keys into Plain Language variable keys.
    
    Required Arguments:
    
    1) path (String) - The path to the folder containing the ECMWF IFS or High Resolution IFS files. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray data array of ECMWF data.    
    
    Plain Language ECMWF IFS/ECMWF High Resolution Variable Keys 
    -------------------------------------------------------------
    
    'total_column_water'
    'total_column_vertically_integrated_water_vapor'
    'total_cloud_cover'
    'snowfall'
    'snow_depth'
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

    """
    clear_idx_files_in_path(path)
    
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
        ds['total_cloud_cover'] = ds['tcc']
        ds = ds.drop_vars('tcc')
    except Exception as e:
        pass
    
    try:
        ds['snowfall'] = ds['sf']
        ds = ds.drop_vars('sf')
    except Exception as e:
        pass
    
    try:
        ds['snow_depth'] = ds['sd']
        ds = ds.drop_vars('sd')
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
        ds['time_maximum_10m_wind_gust'] = ds['fg10']
        ds = ds.drop_vars('fg10')
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
        ds['surface_geopotential_height'] = ds['z']
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
        ds = ds.drop_vars('d2m')
    except Exception as e:
        pass
    
    try:
        ds = ds.drop_vars('t2m')
    except Exception as e:
        pass
    
    clear_idx_files_in_path(path)
        
    return ds


def ecmwf_aifs_post_processing(path,
                            western_bound, 
                            eastern_bound, 
                            northern_bound, 
                            southern_bound):
    
    """
    This function does the following:
    
    1) Subsets the ECMWF AIFS model data. 
    
    2) Post-processes the GRIB variable keys into Plain Language variable keys.
    
    Required Arguments:
    
    1) path (String) - The path to the folder containing the ECMWF AIFS files. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray data array of ECMWF data.    
    
    Plain Language ECMWF AIFS Variable Keys 
    ---------------------------------------
    
    'volumetric_soil_moisture_content'
    'soil_temperature'
    'geopotential_height'
    'specific_humidity'
    'u_wind_component'
    'v_wind_component'
    'air_temperature'
    'vertical velocity'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '10m_u_wind_component'
    '10m_v_wind_component'
    '2m_temperature'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    'water_runoff' 
    'surface_geopotential_height'
    'skin_temperature'
    'surface_pressure'
    'standard_deviation_of_sub_gridscale_orography'
    'slope_of_sub_gridscale_orography'
    'surface_shortwave_radiation_downward'
    'land_sea_mask'
    'surface_longwave_radiation_downward'
    'convective_precipitation'
    'snowfall_water_equivalent'
    'total_precipitation'
    'low_cloud_cover'
    'middle_cloud_cover'
    'high_cloud_cover'
    'total_column_water'
    'total_cloud_cover'
    'mslp'
        
    """
    clear_idx_files_in_path(path)
    
    files = sorted_paths(path)
    
    try:
        ds = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'soilLayer'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
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
                            filter_by_keys={'typeOfLevel': 'heightAboveGround'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
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
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'10u'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
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
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'10v'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
    except Exception as e:
        pass
    
    try:
        ds5 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':167}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
    except Exception as e:
        pass
    
    try:
        ds6 = xr.open_mfdataset(files, 
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
        ds7 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'surface'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
    except Exception as e:
        pass
    
    try:
        ds8 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'lowCloudLayer'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
    except Exception as e:
        pass
    
    try:
        ds9 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'mediumCloudLayer'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
    except Exception as e:
        pass
    
    try:
        ds10 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'highCloudLayer'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
    except Exception as e:
        pass
    
    try:
        ds11 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'entireAtmosphere'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
    except Exception as e:
        pass
    
    try:
        ds12 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'meanSea'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
    except Exception as e:
        pass
    
    
    try:
        ds['volumetric_soil_moisture_content'] = ds['vsw']
        ds = ds.drop_vars('vsw')
    except Exception as e:
        pass
    
    try:
        ds['soil_temperature'] = ds['sot']
        ds = ds.drop_vars('sot')
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height'] = ds1['z']
    except Exception as e:
        pass
    
    try:
        ds['specific_humidity'] = ds1['q']
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component'] = ds1['u']
    except Exception as e:
        pass

    try:
        ds['v_wind_component'] = ds1['v']
    except Exception as e:
        pass
    
    try:
        ds['air_temperature'] = ds1['t']
    except Exception as e:
        pass
    
    try:
        ds['vertical velocity'] = ds1['w']
    except Exception as e:
        pass
    
    try:
        ds['100m_u_wind_component'] = ds2['u100']
    except Exception as e:
        pass
    
    try:
        ds['100m_v_wind_component'] = ds2['v100']
    except Exception as e:
        pass
    
    try:
        ds['10m_u_wind_component'] = ds3['u10']
    except Exception as e:
        pass
    
    try:
        ds['10m_v_wind_component'] = ds4['v10']
    except Exception as e:
        pass
        
    try:
        ds['2m_temperature'] = ds5['t2m']
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point'] = ds6['d2m']
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
        ds['water_runoff'] = ds7['rowe']
    except Exception as e:
        pass
    
    try:
        ds['surface_geopotential_height'] = ds7['z']
    except Exception as e:
        pass
    
    try:
        ds['skin_temperature'] = ds7['skt']
    except Exception as e:
        pass
    
    try:
        ds['surface_pressure'] = ds7['sp']
    except Exception as e:
        pass
    
    try:
        ds['standard_deviation_of_sub_gridscale_orography'] = ds7['sdor']
    except Exception as e:
        pass
    
    try:
        ds['slope_of_sub_gridscale_orography'] = ds7['slor']
    except Exception as e:
        pass
    
    try:
        ds['surface_shortwave_radiation_downward'] = ds7['ssrd']
    except Exception as e:
        pass
    
    try:
        ds['land_sea_mask'] = ds7['lsm']
    except Exception as e:
        pass
    
    try:
        ds['surface_longwave_radiation_downward'] = ds7['strd']
    except Exception as e:
        pass
    
    try:
        ds['convective_precipitation'] = ds7['cp']
    except Exception as e:
        pass
    
    try:
        ds['snowfall_water_equivalent'] = ds7['sf']
    except Exception as e:
        pass
    
    try:
        ds['total_precipitation'] = ds7['tp']
    except Exception as e:
        pass
    
    try:
        ds['low_cloud_cover'] = ds8['lcc']
    except Exception as e:
        pass
    
    try:
        ds['middle_cloud_cover'] = ds9['mcc']
    except Exception as e:
        pass
    
    try:
        ds['high_cloud_cover'] = ds10['hcc']
    except Exception as e:
        pass
    
    try:
        ds['total_column_water'] = ds11['tcw']
    except Exception as e:
        pass
    
    try:
        ds['total_cloud_cover'] = ds11['tcc']
    except Exception as e:
        pass
    
    try:
        ds['mslp'] = ds12['msl']
    except Exception as e:
        pass
    
    
    clear_idx_files_in_path(path)
    
    return ds

def ecmwf_ifs_wave_post_processing(path,
                            western_bound, 
                            eastern_bound, 
                            northern_bound, 
                            southern_bound):
    
    """
    This function does the following:
    
    1) Subsets the ECMWF IFS Wave model data. 
    
    2) Post-processes the GRIB variable keys into Plain Language variable keys.
    
    Required Arguments:
    
    1) path (String) - The path to the folder containing the ECMWF IFS Wave files. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray data array of ECMWF data.    
    
    Plain Language ECMWF IFS Wave Variable Keys 
    -------------------------------------------
    
    'mean_zero_crossing_wave_period'
    'significant_height_of_combined_waves_and_swell'
    'mean_wave_direction'
    'peak_wave_period'
    'mean_wave_period'

    """
    clear_idx_files_in_path(path)
    
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
        ds['mean_zero_crossing_wave_period'] = ds['mp2']
        ds = ds.drop_vars('mp2')
    except Exception as e:
        pass
    
    try:
        ds['significant_height_of_combined_waves_and_swell'] = ds['swh']
        ds = ds.drop_vars('swh')
    except Exception as e:
        pass
    
    try:
        ds['mean_wave_direction'] = ds['mwd']
        ds = ds.drop_vars('mwd')
    except Exception as e:
        pass
    
    try:
        ds['peak_wave_period'] = ds['pp1d']
        ds = ds.drop_vars('pp1d')
    except Exception as e:
        pass
    
    try:
        ds['mean_wave_period'] = ds['mwp']
        ds = ds.drop_vars('mwp')
    except Exception as e:
        pass
    
    clear_idx_files_in_path(path)
    
    return ds