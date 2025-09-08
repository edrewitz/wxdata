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

from wxdata.gfs.paths import get_branch_path
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
    
    paths = get_branch_path(model, cat, step, directory)

    if model == 'GEFS0P50':
        
        if directory == 'ATMOS':
    
            ds_list_1 = []
            
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
            ds['mixed_layer_cape'] = ds['cape']
            ds['mixed_layer_cin'] = ds['cin']
                        
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
                'v',
                'cape',
                'cin']
                )
                
        else:
            path = paths
            file_pattern = file_pattern = f"{path}/*.grib2"
            ds = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False)
            ds = shift_longitude(ds)
            ds = ds.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
            
            ds['fine_particulates'] = ds['pmtf']
            ds['coarse_particulates'] = ds['pmtc']
            
            ds = ds.drop_vars(
                ['pmtf',
                 'pmtc']
            )
            
        
    if model == 'GEFS0P50 SECONDARY PARAMETERS':
        
        if ensemble == False:
            
            path = paths
            file_pattern = f"{path}/*.grib2"
            
            ds = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'surface'})
            ds = shift_longitude(ds)
            ds = ds.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['surface_temperature'] = ds['t']
            ds['surface_visibility'] = ds['vis']
            ds['surface_wind_gust'] = ds['gust']
            ds['haines_index'] = ds['hindex']
            ds['plant_canopy_surface_water'] = ds['cnwat']
            ds['snow_cover'] = ds['snowc']
            ds['percent_frozen_precipitation'] = ds['cpofp']
            ds['snow_phase_change_heat_flux'] = ds['snohf']
            ds['surface_roughness'] = ds['fsr']
            ds['frictional_velocity'] = ds['fricv']
            ds['wilting_point'] = ds['wilt']
            ds['field_capacity'] = ds['fldcp']
            ds['sunshine_duration'] = ds['SUNSD']
            ds['surface_lifted_index'] = ds['lftx']
            ds['best_4_layer_lifted_index'] = ds['lftx4']
            ds['land_sea_mask'] = ds['lsm']
            ds['sea_ice_area_friction'] = ds['siconc']
            ds['orography'] = ds['orog']
            ds['surface_cape'] = ds['cape']
            ds['surface_cin'] = ds['cin']
            ds['convective_precipitation_rate'] = ds['cpr']
            ds['precipitation_rate'] = ds['prate']
            ds['total_convective_precipitation'] = ds['acpcp']
            ds['total_non_convective_precipitation'] = ds['ncpcp']
            ds['total_precipitation'] = ds['total_convective_precipitation'] + ds['total_non_convective_precipitation']
            ds['water_runoff'] = ds['watr']
            ds['ground_heat_flux'] = ds['gflux']
            ds['time_mean_u_component_of_atmospheric_surface_momentum_flux'] = ds['avg_utaua']
            ds['time_mean_v_component_of_atmospheric_surface_momentum_flux'] = ds['avg_vtaua']
            ds['instantaneous_eastward_gravity_wave_surface_flux'] = ds['iegwss']
            ds['instantaneous_northward_gravity_wave_surface_flux'] = ds['ingwss']
            ds['uv_b_downward_solar_flux'] = ds['duvb']
            ds['clear_sky_uv_b_downward_solar_flux'] = ds['cduvb']
            ds['average_surface_albedo'] = ds['avg_al']
            
            
            ds = ds.drop_vars(
                
                ['t',
                 'vis',
                 'gust',
                 'hindex',
                 'cnwat', 
                 'unknown',
                 'snowc',
                 'cpofp',
                 'snohf',
                 'fsr',
                 'fricv',
                 'wilt',
                 'fldcp',
                 'SUNSD',
                 'lftx',
                 'lftx4',
                 'lsm',
                 'siconc',
                 'orog',
                 'cape',
                 'cin',
                 'cpr',
                 'prate',
                 'acpcp',
                 'ncpcp',
                 'watr',
                 'gflux',
                 'avg_utaua',
                 'avg_vtaua',
                 'iegwss',
                 'ingwss',
                 'duvb',
                 'cduvb',
                 'avg_al']
                
                ) 
            
            ds1 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'meanSea'})
            ds1 = shift_longitude(ds1)
            ds1 = ds1.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))   
            ds['mslp'] = ds1['msl']
            ds['mslp_eta_reduction'] = ds1['mslet']   
            
            ds2 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'planetaryBoundaryLayer'})
            ds2 = shift_longitude(ds2)
            ds2 = ds2.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))   
            ds['boundary_layer_u_wind_component'] = ds2['u']
            ds['boundary_layer_v_wind_component'] = ds2['v']
            ds['ventilation_rate'] = ds2['VRATE']             
            
            ds3 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
            ds3 = shift_longitude(ds3)
            ds3 = ds3.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))    
            ds['geopotential_height'] = ds3['gh']
            
            ds4 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'t'})
            ds4 = shift_longitude(ds4)
            ds4 = ds4.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['air_temperature'] = ds4['t']            
            
            ds5 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'w'})
            ds5 = shift_longitude(ds5)
            ds5 = ds5.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['vertical_velocity'] = ds5['w']
            
            ds6 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'u'})
            ds6 = shift_longitude(ds6)
            ds6 = ds6.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['u_wind_component'] = ds6['u']
            
            ds7 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'v'})
            ds7 = shift_longitude(ds7)
            ds7 = ds7.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['v_wind_component'] = ds7['v'] 
            
            ds8 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'o3mr'})
            ds8 = shift_longitude(ds8)
            ds8 = ds8.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['ozone_mixing_ratio'] = ds8['o3mr']
            
            ds9 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'absv'})
            ds9 = shift_longitude(ds9)
            ds9 = ds9.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['absolute_vorticity'] = ds9['absv']
            
            ds10 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'clwmr'})
            ds10 = shift_longitude(ds10)
            ds10 = ds10.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['cloud_mixing_ratio'] = ds10['clwmr']
            
            ds12 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'ICSEV'})
            ds12 = shift_longitude(ds12)
            ds12 = ds12.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['icing_severity'] = ds12['ICSEV']
            
            ds13 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'tcc'})
            ds13 = shift_longitude(ds13)
            ds13 = ds13.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['total_cloud_cover'] = ds13['tcc']
            
            ds14 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'r'})
            ds14 = shift_longitude(ds14)
            ds14 = ds14.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['relative_humidity'] = ds14['r']
            
            ds15 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'depthBelowLandLayer'})
            ds15 = shift_longitude(ds15)
            ds15 = ds15.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['liquid_volumetric_soil_moisture_non_frozen'] = ds15['soill']
            
            ds16 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'depthBelowLandLayer', 'shortName':'st'})
            ds16 = shift_longitude(ds16)
            ds16 = ds16.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['soil_temperature'] = ds16['st']
            
            ds17 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'depthBelowLandLayer', 'shortName':'soilw'})
            ds17 = shift_longitude(ds17)
            ds17 = ds17.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['volumetric_soil_moisture_content'] = ds17['soilw']
            
            ds18 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround'})
            ds18 = shift_longitude(ds18)
            ds18 = ds18.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['2m_specific_humidity'] = ds18['sh2']
            ds['2m_dew_point'] = ds18['d2m']
            ds['2m_apparent_temperature'] = ds18['aptmp']
            
            ds19 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'q'})
            ds19 = shift_longitude(ds19)
            ds19 = ds19.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['80m_specific_humidity'] = ds19['q']
            
            ds20 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'t'})
            ds20 = shift_longitude(ds20)
            ds20 = ds20.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['80m_and_100m_temperature'] = ds20['t']
            
            ds21 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'pres'})
            ds21 = shift_longitude(ds21)
            ds21 = ds21.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['80m_air_pressure'] = ds21['pres']
            
            ds22 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'u'})
            ds22= shift_longitude(ds22)
            ds22 = ds22.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['80m_u_wind_component'] = ds22['u']
            
            ds23 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'v'})
            ds23 = shift_longitude(ds23)
            ds23 = ds23.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['80m_v_wind_component'] = ds23['v']
            
            ds24 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'atmosphereSingleLayer'})
            ds24 = shift_longitude(ds24)
            ds24 = ds24.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['atmosphere_single_layer_relative_humidity'] = ds24['r']
            ds['cloud_water'] = ds24['cwat']
            ds['total_ozone'] = ds24['tozne']
            
            ds25 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'cloudCeiling'})
            ds25 = shift_longitude(ds25)
            ds25 = ds25.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['cloud_ceiling_height'] = ds25['gh']
            
            ds26 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'nominalTop'})
            ds26 = shift_longitude(ds26)
            ds26 = ds26.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
            ds['brightness_temperature'] = ds26['btmp']
            
            ds27 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer'})
            ds27 = shift_longitude(ds27)
            ds27 = ds27.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['3km_helicity'] = ds27['hlcy'] 
            
            ds28 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer', 'shortName':'ustm'})
            ds28 = shift_longitude(ds28)
            ds28 = ds28.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['u_component_of_storm_motion'] = ds28['ustm']
            
            ds29 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer', 'shortName':'vstm'})
            ds29 = shift_longitude(ds29)
            ds29 = ds29.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
            ds['v_component_of_storm_motion'] = ds29['vstm']
            
            ds30 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'tropopause'})
            ds30 = shift_longitude(ds30)
            ds30 = ds30.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['tropopause_height'] = ds30['gh']
            ds['tropopause_pressure'] = ds30['trpp']
            ds['tropopause_standard_atmosphere_reference_height'] = ds30['icaht']
            ds['tropopause_u_wind_component'] = ds30['u']
            ds['tropopause_v_wind_component'] = ds30['v']
            ds['tropopause_temperature'] = ds30['t']
            ds['tropopause_vertical_speed_shear'] = ds30['vwsh']
            
            ds31 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'maxWind'})
            ds31 = shift_longitude(ds31)
            ds31 = ds31.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['max_wind_u_component'] = ds31['u']
            ds['max_wind_v_component'] = ds31['v']
            
            ds32 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isothermZero'})
            ds32 = shift_longitude(ds32)
            ds32 = ds32.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['zero_deg_c_isotherm_geopotential_height'] = ds32['gh']
            ds['zero_deg_c_isotherm_relative_humidity'] = ds32['r']
            
            ds33 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'highestTroposphericFreezing'})
            ds33 = shift_longitude(ds33)
            ds33 = ds33.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['highest_tropospheric_freezing_level_geopotential_height'] = ds33['gh']
            ds['highest_tropospheric_freezing_level_relative_humidity'] = ds33['r']
            
            ds34 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'sigmaLayer'})
            ds34 = shift_longitude(ds33)
            ds34 = ds34.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['relative_humdity_by_sigma_layer'] = ds34['r']
            
            ds35 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'sigma'})
            ds35 = shift_longitude(ds35)
            ds35 = ds35.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['995_sigma_relative_humdity'] = ds35['r']
            ds['995_sigma_temperature'] = ds35['t']
            ds['995_sigma_theta'] = ds35['pt']
            ds['995_u_wind_component'] = ds35['u']
            ds['995_v_wind_component'] = ds35['v']
            ds['995_vertical_velocity'] = ds35['w']
            
            ds36 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'theta'})
            ds36 = shift_longitude(ds36)
            ds36 = ds36.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['potential_vorticity'] = ds36['pv']
            
            ds37 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'theta', 'shortName':'u'})
            ds37 = shift_longitude(ds37)
            ds37 = ds37.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['theta_level_u_wind_component'] = ds37['u']
            
            ds38 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'theta', 'shortName':'v'})
            ds38 = shift_longitude(ds38)
            ds38 = ds38.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['theta_level_v_wind_component'] = ds38['v']
            
            ds39 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'theta', 'shortName':'t'})
            ds39 = shift_longitude(ds39)
            ds39 = ds39.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['theta_level_temperature'] = ds39['t']
            
            ds40 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'theta', 'shortName':'mont'})
            ds40 = shift_longitude(ds40)
            ds40 = ds40.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['theta_level_montgomery_potential'] = ds40['mont']
            
            ds41 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'potentialVorticity'})
            ds41 = shift_longitude(ds41)
            ds41 = ds41.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['potential_vorticity_level_u_wind_component'] = ds41['u']
            ds['potential_vorticity_level_v_wind_component'] = ds41['v']
            ds['potential_vorticity_level_temperature'] = ds41['t']
            ds['potential_vorticity_level_geopotential_height'] = ds41['gh']
            ds['potential_vorticity_level_air_pressure'] = ds41['pres']
            ds['potential_vorticity_level_vertical_speed_shear'] = ds41['vwsh']
            
            ds42 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'})
            ds42 = shift_longitude(ds42)
            ds42 = ds42.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['mixed_layer_air_temperature'] = ds42['t']
            ds['mixed_layer_relative_humidity'] = ds42['r']
            ds['mixed_layer_specific_humidity'] = ds42['q']
            ds['mixed_layer_u_wind_component'] = ds42['u']
            ds['mixed_layer_v_wind_component'] = ds42['v']
            
            ds43 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'dpt'})
            ds43 = shift_longitude(ds43)
            ds43 = ds43.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['mixed_layer_dew_point'] = ds43['dpt']
            
            ds44 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'pwat'})
            ds44 = shift_longitude(ds44)
            ds44 = ds44.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['mixed_layer_precipitable_water'] = ds44['pwat']
            
            ds45 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'pli'})
            ds45 = shift_longitude(ds45)
            ds45 = ds45.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['parcel_lifted_index_to_500hPa'] = ds45['pli']
            
            ds46 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'cape'})
            ds46 = shift_longitude(ds46)
            ds46 = ds46.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['mixed_layer_cape'] = ds46['cape']
            
            ds47 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'cin'})
            ds47 = shift_longitude(ds47)
            ds47 = ds47.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['mixed_layer_cin'] = ds47['cin']
            
            ds48 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'plpl'})
            ds48 = shift_longitude(ds48)
            ds48 = ds48.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
            ds['pressure_level_from_which_a_parcel_was_lifted'] = ds48['plpl']
            
        else:
            
            ds_list_1 = []      
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'surface'})
                ds = shift_longitude(ds)
                ds = ds.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_1.append(ds)
            
            ds_list_2 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds1 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'meanSea'})
                ds1 = shift_longitude(ds1)
                ds1 = ds1.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))   
                ds_list_2.append(ds1)

            ds_list_3 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds2 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'planetaryBoundaryLayer'})
                ds2 = shift_longitude(ds2)
                ds2 = ds2.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))   
                ds_list_3.append(ds2)
           
            ds_list_4 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds3 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
                ds3 = shift_longitude(ds3)
                ds3 = ds3.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_4.append(ds3)  
            
            ds_list_5 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds4 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'t'})
                ds4 = shift_longitude(ds4)
                ds4 = ds4.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_5.append(ds4)
                     
            ds_list_6 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds5 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'w'})
                ds5 = shift_longitude(ds5)
                ds5 = ds5.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_6.append(ds5)
            
            ds_list_7 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds6 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'u'})
                ds6 = shift_longitude(ds6)
                ds6 = ds6.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_7.append(ds6)  
            
            ds_list_8 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds7 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'v'})
                ds7 = shift_longitude(ds7)
                ds7 = ds7.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_8.append(ds7)
            
            ds_list_9 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds8 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'o3mr'})
                ds8 = shift_longitude(ds8)
                ds8 = ds8.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_9.append(ds8) 
            
            ds_list_10 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds9 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'absv'})
                ds9 = shift_longitude(ds9)
                ds9 = ds9.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_10.append(ds9)
            
            ds_list_11 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds10 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'clwmr'})
                ds10 = shift_longitude(ds10)
                ds10 = ds10.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_11.append(ds10)  
            
            ds_list_12 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds12 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'ICSEV'})
                ds12 = shift_longitude(ds12)
                ds12 = ds12.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_12.append(ds12) 
            
            ds_list_13 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds13 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'tcc'})
                ds13 = shift_longitude(ds13)
                ds13 = ds13.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_13.append(ds13)
            
            ds_list_14 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds14 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'r'})
                ds14 = shift_longitude(ds14)
                ds14 = ds14.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_14.append(ds14)
            
            ds_list_15 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds15 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'depthBelowLandLayer'})
                ds15 = shift_longitude(ds15)
                ds15 = ds15.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_15.append(ds15) 
            
            ds_list_16 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds16 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'depthBelowLandLayer', 'shortName':'st'})
                ds16 = shift_longitude(ds16)
                ds16 = ds16.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_16.append(ds16)
            
            ds_list_17 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds17 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'depthBelowLandLayer', 'shortName':'soilw'})
                ds17 = shift_longitude(ds17)
                ds17 = ds17.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_17.append(ds17)
            
            ds_list_18 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds18 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround'})
                ds18 = shift_longitude(ds18)
                ds18 = ds18.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_18.append(ds18)
            
            ds_list_19 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds19 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'q'})
                ds19 = shift_longitude(ds19)
                ds19 = ds19.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_19.append(ds19)                
            
            ds_list_20 = []
            for path in paths:
                ds20 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'t'})
                ds20 = shift_longitude(ds20)
                ds20 = ds20.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_20.append(ds20)            
            
            ds_list_21 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds21 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'pres'})
                ds21 = shift_longitude(ds21)
                ds21 = ds21.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_21.append(ds21)            
            
            ds_list_22 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds22 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'u'})
                ds22 = shift_longitude(ds22)
                ds22 = ds22.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_22.append(ds22)            
            
            ds_list_23 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds23 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'v'})
                ds23 = shift_longitude(ds23)
                ds23 = ds23.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_23.append(ds23)            
            
            ds_list_24 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds24 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'atmosphereSingleLayer'})
                ds24 = shift_longitude(ds24)
                ds24 = ds24.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_24.append(ds24)

            ds_list_25= []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds25 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'cloudCeiling'})
                ds25 = shift_longitude(ds25)
                ds25 = ds25.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_25.append(ds25)            
            
            ds_list_26 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds26 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'nominalTop'})
                ds26 = shift_longitude(ds26)
                ds26 = ds26.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                ds_list_26.append(ds26)            
            
            ds_list_27 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds27 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer'})
                ds27 = shift_longitude(ds27)
                ds27 = ds27.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_27.append(ds27)            
            
            ds_list_28 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds28 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer', 'shortName':'ustm'})
                ds28 = shift_longitude(ds28)
                ds28 = ds28.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_28.append(ds28)            
            
            ds_list_29 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds29 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer', 'shortName':'vstm'})
                ds29 = shift_longitude(ds29)
                ds29 = ds29.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))  
                ds_list_29.append(ds29)            
            
            ds_list_30 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds30 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'tropopause'})
                ds30 = shift_longitude(ds30)
                ds30 = ds30.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_30.append(ds30)

            ds_list_31 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds31 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'maxWind'})
                ds31 = shift_longitude(ds31)
                ds31 = ds31.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_31.append(ds31)
            
            ds_list_32 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds32 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isothermZero'})
                ds32 = shift_longitude(ds32)
                ds32 = ds32.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_32.append(ds32)

            ds_list_33 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds33 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'highestTroposphericFreezing'})
                ds33 = shift_longitude(ds33)
                ds33 = ds33.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_33.append(ds33)  
            
            ds_list_34 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds34 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'sigmaLayer'})
                ds34 = shift_longitude(ds33)
                ds34 = ds34.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_34.append(ds34)            
            
            ds_list_35 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds35 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'sigma'})
                ds35 = shift_longitude(ds35)
                ds35 = ds35.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_35.append(ds35)
            
            ds_list_36 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds36 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'theta'})
                ds36 = shift_longitude(ds36)
                ds36 = ds36.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_36.append(ds36)            
            
            ds_list_37 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds37 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'theta', 'shortName':'u'})
                ds37 = shift_longitude(ds37)
                ds37 = ds37.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_37.append(ds37)            
            
            ds_list_38 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds38 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'theta', 'shortName':'v'})
                ds38 = shift_longitude(ds38)
                ds38 = ds38.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_38.append(ds38)            
            
            ds_list_39 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds39 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'theta', 'shortName':'t'})
                ds39 = shift_longitude(ds39)
                ds39 = ds39.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_39.append(ds39)            
            
            ds_list_40 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds40 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'theta', 'shortName':'mont'})
                ds40 = shift_longitude(ds40)
                ds40 = ds40.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_40.append(ds40)            
            
            ds_list_41 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds41 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'potentialVorticity'})
                ds41 = shift_longitude(ds41)
                ds41 = ds41.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_41.append(ds41)
            
            ds_list_42 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds42 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'})
                ds42 = shift_longitude(ds42)
                ds42 = ds42.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_42.append(ds42)
            
            ds_list_43 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds43 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'dpt'})
                ds43 = shift_longitude(ds43)
                ds43 = ds43.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_43.append(ds43)            
            
            ds_list_44 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds44 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'pwat'})
                ds44 = shift_longitude(ds44)
                ds44 = ds44.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_44.append(ds44)            
            
            ds_list_45 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds45 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'pli'})
                ds45 = shift_longitude(ds45)
                ds45 = ds45.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_45.append(ds45)            
            
            ds_list_46 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds46 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'cape'})
                ds46 = shift_longitude(ds46)
                ds46 = ds46.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_46.append(ds46)            
            
            ds_list_47 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds47 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'cin'})
                ds47 = shift_longitude(ds47)
                ds47 = ds47.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_47.append(ds47)            
            
            ds_list_48 = []
            for path in paths:
                file_pattern = f"{path}/*.grib2"
                ds48 = xr.open_mfdataset(file_pattern, concat_dim='step', combine='nested', coords='minimal', engine='cfgrib', compat='override', decode_timedelta=False, filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'plpl'})
                ds48 = shift_longitude(ds48)
                ds48 = ds48.sel(longitude=slice(western_bound, eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1)) 
                ds_list_48.append(ds48)            
        
        
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
            ds12 = xr.concat(ds_list_12, dim='number')
            ds13 = xr.concat(ds_list_13, dim='number')
            ds14 = xr.concat(ds_list_14, dim='number')
            ds15 = xr.concat(ds_list_15, dim='number')
            ds16 = xr.concat(ds_list_16, dim='number')
            ds17 = xr.concat(ds_list_17, dim='number')
            ds18 = xr.concat(ds_list_18, dim='number')
            ds19 = xr.concat(ds_list_19, dim='number')
            ds20 = xr.concat(ds_list_20, dim='number')
            ds21 = xr.concat(ds_list_21, dim='number')
            ds22 = xr.concat(ds_list_22, dim='number')
            ds23 = xr.concat(ds_list_23, dim='number')
            ds24 = xr.concat(ds_list_24, dim='number')
            ds25 = xr.concat(ds_list_25, dim='number')
            ds26 = xr.concat(ds_list_26, dim='number')
            ds27 = xr.concat(ds_list_27, dim='number')
            ds28 = xr.concat(ds_list_28, dim='number')
            ds29 = xr.concat(ds_list_29, dim='number')
            ds30 = xr.concat(ds_list_30, dim='number')
            ds31 = xr.concat(ds_list_31, dim='number')
            ds32 = xr.concat(ds_list_32, dim='number')
            ds33 = xr.concat(ds_list_33, dim='number')
            ds34 = xr.concat(ds_list_34, dim='number')
            ds35 = xr.concat(ds_list_35, dim='number')
            ds36 = xr.concat(ds_list_36, dim='number')
            ds37 = xr.concat(ds_list_37, dim='number')
            ds38 = xr.concat(ds_list_38, dim='number')
            ds39 = xr.concat(ds_list_39, dim='number')
            ds40 = xr.concat(ds_list_40, dim='number')
            ds41 = xr.concat(ds_list_41, dim='number')
            ds42 = xr.concat(ds_list_42, dim='number')
            ds43 = xr.concat(ds_list_43, dim='number')
            ds44 = xr.concat(ds_list_44, dim='number')
            ds45 = xr.concat(ds_list_45, dim='number')
            ds46 = xr.concat(ds_list_46, dim='number')
            ds47 = xr.concat(ds_list_47, dim='number')
            ds48 = xr.concat(ds_list_48, dim='number')
                         
            
            
            ds['surface_temperature'] = ds['t']
            ds['surface_visibility'] = ds['vis']
            ds['surface_wind_gust'] = ds['gust']
            ds['haines_index'] = ds['hindex']
            ds['plant_canopy_surface_water'] = ds['cnwat']
            ds['snow_cover'] = ds['snowc']
            ds['percent_frozen_precipitation'] = ds['cpofp']
            ds['snow_phase_change_heat_flux'] = ds['snohf']
            ds['surface_roughness'] = ds['fsr']
            ds['frictional_velocity'] = ds['fricv']
            ds['wilting_point'] = ds['wilt']
            ds['field_capacity'] = ds['fldcp']
            ds['sunshine_duration'] = ds['SUNSD']
            ds['surface_lifted_index'] = ds['lftx']
            ds['best_4_layer_lifted_index'] = ds['lftx4']
            ds['land_sea_mask'] = ds['lsm']
            ds['sea_ice_area_friction'] = ds['siconc']
            ds['orography'] = ds['orog']
            ds['surface_cape'] = ds['cape']
            ds['surface_cin'] = ds['cin']
            ds['convective_precipitation_rate'] = ds['cpr']
            ds['precipitation_rate'] = ds['prate']
            ds['total_convective_precipitation'] = ds['acpcp']
            ds['total_non_convective_precipitation'] = ds['ncpcp']
            ds['total_precipitation'] = ds['total_convective_precipitation'] + ds['total_non_convective_precipitation']
            ds['water_runoff'] = ds['watr']
            ds['ground_heat_flux'] = ds['gflux']
            ds['time_mean_u_component_of_atmospheric_surface_momentum_flux'] = ds['avg_utaua']
            ds['time_mean_v_component_of_atmospheric_surface_momentum_flux'] = ds['avg_vtaua']
            ds['instantaneous_eastward_gravity_wave_surface_flux'] = ds['iegwss']
            ds['instantaneous_northward_gravity_wave_surface_flux'] = ds['ingwss']
            ds['uv_b_downward_solar_flux'] = ds['duvb']
            ds['clear_sky_uv_b_downward_solar_flux'] = ds['cduvb']
            ds['average_surface_albedo'] = ds['avg_al']
            
            ds['mslp'] = ds1['msl']
            ds['mslp_eta_reduction'] = ds1['mslet']  
            ds['boundary_layer_u_wind_component'] = ds2['u']
            ds['boundary_layer_v_wind_component'] = ds2['v']
            ds['ventilation_rate'] = ds2['VRATE']   
            ds['geopotential_height'] = ds3['gh']
            ds['air_temperature'] = ds4['t']   
            ds['vertical_velocity'] = ds5['w']
            ds['u_wind_component'] = ds6['u']
            ds['v_wind_component'] = ds7['v'] 
            ds['ozone_mixing_ratio'] = ds8['o3mr']
            ds['absolute_vorticity'] = ds9['absv']
            ds['cloud_mixing_ratio'] = ds10['clwmr']
            ds['icing_severity'] = ds12['ICSEV']
            ds['total_cloud_cover'] = ds13['tcc']
            ds['relative_humidity'] = ds14['r']
            ds['liquid_volumetric_soil_moisture_non_frozen'] = ds15['soill']
            ds['soil_temperature'] = ds16['st']
            ds['volumetric_soil_moisture_content'] = ds17['soilw']
            ds['2m_specific_humidity'] = ds18['sh2']
            ds['2m_dew_point'] = ds18['d2m']
            ds['2m_apparent_temperature'] = ds18['aptmp']
            ds['80m_specific_humidity'] = ds19['q']
            ds['80m_air_pressure'] = ds21['pres']
            ds['80m_u_wind_component'] = ds22['u']
            ds['80m_v_wind_component'] = ds23['v']
            ds['atmosphere_single_layer_relative_humidity'] = ds24['r']
            ds['cloud_water'] = ds24['cwat']
            ds['total_ozone'] = ds24['tozne']
            ds['cloud_ceiling_height'] = ds25['gh']
            ds['brightness_temperature'] = ds26['btmp']
            ds['3km_helicity'] = ds27['hlcy'] 
            ds['u_component_of_storm_motion'] = ds28['ustm']
            ds['v_component_of_storm_motion'] = ds29['vstm']
            ds['tropopause_height'] = ds30['gh']
            ds['tropopause_pressure'] = ds30['trpp']
            ds['tropopause_standard_atmosphere_reference_height'] = ds30['icaht']
            ds['tropopause_u_wind_component'] = ds30['u']
            ds['tropopause_v_wind_component'] = ds30['v']
            ds['tropopause_temperature'] = ds30['t']
            ds['tropopause_vertical_speed_shear'] = ds30['vwsh']
            ds['max_wind_u_component'] = ds31['u']
            ds['max_wind_v_component'] = ds31['v']
            ds['zero_deg_c_isotherm_geopotential_height'] = ds32['gh']
            ds['zero_deg_c_isotherm_relative_humidity'] = ds32['r']
            ds['highest_tropospheric_freezing_level_geopotential_height'] = ds33['gh']
            ds['highest_tropospheric_freezing_level_relative_humidity'] = ds33['r']
            ds['995_sigma_relative_humdity'] = ds35['r']
            ds['995_sigma_temperature'] = ds35['t']
            ds['995_sigma_theta'] = ds35['pt']
            ds['995_u_wind_component'] = ds35['u']
            ds['995_v_wind_component'] = ds35['v']
            ds['995_vertical_velocity'] = ds35['w']
            ds['potential_vorticity'] = ds36['pv']
            ds['theta_level_u_wind_component'] = ds37['u']
            ds['theta_level_v_wind_component'] = ds38['v']
            ds['theta_level_temperature'] = ds39['t']
            ds['theta_level_montgomery_potential'] = ds40['mont']
            ds['potential_vorticity_level_u_wind_component'] = ds41['u']
            ds['potential_vorticity_level_v_wind_component'] = ds41['v']
            ds['potential_vorticity_level_temperature'] = ds41['t']
            ds['potential_vorticity_level_geopotential_height'] = ds41['gh']
            ds['potential_vorticity_level_air_pressure'] = ds41['pres']
            ds['potential_vorticity_level_vertical_speed_shear'] = ds41['vwsh']
            ds['mixed_layer_air_temperature'] = ds42['t']
            ds['mixed_layer_relative_humidity'] = ds42['r']
            ds['mixed_layer_specific_humidity'] = ds42['q']
            ds['mixed_layer_u_wind_component'] = ds42['u']
            ds['mixed_layer_v_wind_component'] = ds42['v']
            ds['mixed_layer_dew_point'] = ds43['dpt']
            ds['mixed_layer_precipitable_water'] = ds44['pwat']
            ds['parcel_lifted_index_to_500hPa'] = ds45['pli']
            ds['mixed_layer_cape'] = ds46['cape']
            ds['mixed_layer_cin'] = ds47['cin']
            ds['pressure_level_from_which_a_parcel_was_lifted'] = ds48['plpl']            
            
            ds = ds.drop_vars(
                
                ['t',
                 'vis',
                 'gust',
                 'hindex',
                 'cnwat', 
                 'unknown',
                 'snowc',
                 'cpofp',
                 'snohf',
                 'fsr',
                 'fricv',
                 'wilt',
                 'fldcp',
                 'SUNSD',
                 'lftx',
                 'lftx4',
                 'lsm',
                 'siconc',
                 'orog',
                 'cape',
                 'cin',
                 'cpr',
                 'prate',
                 'acpcp',
                 'ncpcp',
                 'watr',
                 'gflux',
                 'avg_utaua',
                 'avg_vtaua',
                 'iegwss',
                 'ingwss',
                 'duvb',
                 'cduvb',
                 'avg_al']
                
                ) 
    
    return ds
