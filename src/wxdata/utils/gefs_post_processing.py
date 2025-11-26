"""
This file hosts the functions responsible for GEFS data post-processing. 

GRIB variable keys will be post-processed into Plain Language variable keys. 

(C) Eric J. Drewitz 2025
"""
import xarray as xr
import glob
import sys
import logging
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from wxdata.utils.file_funcs import(
    file_paths_for_xarray,
    clear_gefs_idx_files
)

from wxdata.utils.coords import shift_longitude

sys.tracebacklimit = 0
logging.disable()

def primary_gefs_post_processing(paths):
    
    """
    This function post-processes the GEFS (Primary) Parameters for GEFS0P50 and GEFS0P25. 
    
    Required Arguments: 
    
    1) paths (List) - A list of file paths to the GEFS0P50 or GEFS0P25 files. 
    
    Returns
    -------
    
    An xarray data array of the post-processed GEFS data. 
    GRIB Keys are converted to Plain Language Keys. 
    
    New Variable Keys After Post-Processing (Decrypted GRIB Keys Into Plain Language)
    --------------------------------------------------------------------------------
    
    GEFS0P50
    --------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'mixed_layer_cape'
    'mixed_layer_cin'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'u_wind_component'
    'v_wind_component'
    
    GEFS0P25
    --------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'surface_visibility'
    'surface_wind_gust'
    'percent_frozen_precipitation'
    'surface_cape'
    'surface_cin'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    '2m_dew_point'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'mixed_layer_cape'
    'mixed_layer_cin'
    '3km_helicity'
    
    """

    clear_gefs_idx_files(paths)

    if len(paths) > 1:
        
        paths = file_paths_for_xarray(paths)
        try:
            ds_list_1 = []
            
            for path in paths:
                file_pattern = path
                ds1 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step', 
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False, 
                                        filter_by_keys={'typeOfLevel': 'surface'})
                ds1 = shift_longitude(ds1)
                ds_list_1.append(ds1)
        except Exception as e:
            pass
        try:
            ds_list_2 = []
            for path in paths:
                file_pattern = path
                ds2 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step', 
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False, 
                                        filter_by_keys={'typeOfLevel': 'meanSea'})
                ds2 = shift_longitude(ds2)
                ds_list_2.append(ds2)
        except Exception as e:
            pass                
        try:
            ds_list_3 = []
            for path in paths:
                file_pattern = path
                ds3 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step', 
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False, 
                                        filter_by_keys={'typeOfLevel': 'depthBelowLandLayer'})
                ds3 = shift_longitude(ds3)
                ds_list_3.append(ds3)
        except Exception as e:
            pass                
        try:
            ds_list_4 = []
            for path in paths:
                file_pattern = path
                ds4 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step', 
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False, 
                                        filter_by_keys={'typeOfLevel': 'heightAboveGround'})
                ds4 = shift_longitude(ds4)
                ds_list_4.append(ds4)
        except Exception as e:
            pass       
        
        try:
            ds_list_5 = []
            for path in paths:
                file_pattern = path
                ds5 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step', 
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False, 
                                        filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'10u'})
                ds5 = shift_longitude(ds5)
                ds_list_5.append(ds5)
        except Exception as e:
            pass  
        
        try:
            ds_list_6 = []
            for path in paths:
                file_pattern = path
                ds6 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step', 
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False, 
                                        filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'10v'})
                ds6 = shift_longitude(ds6)
                ds_list_6.append(ds6)
        except Exception as e:
            pass           

        try:
            ds_list_7 = []
            for path in paths:
                file_pattern = path
                ds7 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step', 
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False, 
                                        filter_by_keys={'typeOfLevel': 'atmosphereSingleLayer'})
                ds7 = shift_longitude(ds7)
                ds_list_7.append(ds7)
        except Exception as e:
            pass    
        try:
            ds_list_8 = []
            for path in paths:
                file_pattern = path
                ds8 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step', 
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False, 
                                        filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'})
                ds8 = shift_longitude(ds8)
                ds_list_8.append(ds8)
        except Exception as e:
            pass    
        try:
            ds_list_9 = []
            for path in paths:
                file_pattern = path
                ds9 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step', 
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False, 
                                        filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
                ds9 = shift_longitude(ds9)
                ds_list_9.append(ds9)
        except Exception as e:
            pass    
        try:
            ds_list_10 = []
            for path in paths:
                file_pattern = path
                ds10 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step', 
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'t'})
                ds10 = shift_longitude(ds10)
                ds_list_10.append(ds10)
        except Exception as e:
            pass    
        try:
            ds_list_11 = []
            for path in paths:
                file_pattern = path
                ds11 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step', 
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'r'})
                ds11 = shift_longitude(ds11)
                ds_list_11.append(ds11)
        except Exception as e:
            pass    
        try:
            ds_list_12 = []
            for path in paths:
                file_pattern = path
                ds12 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step', 
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'u'})
                ds12 = shift_longitude(ds12)
                ds_list_12.append(ds12)
        except Exception as e:
            pass    
        try:
            ds_list_13 = []
            for path in paths:
                file_pattern = path
                ds13 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step', 
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'v'})
                ds13 = shift_longitude(ds13)
                ds_list_13.append(ds13)
        except Exception as e:
            pass   
        
        try:
            ds_list_14 = []
            for path in paths:
                file_pattern = path
                ds14 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step', 
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer'})
                ds14 = shift_longitude(ds14)
                ds_list_14.append(ds14)
        except Exception as e:
            pass                       
        

        try:
            ds = xr.concat(ds_list_1, 
                           dim='number')
        except Exception as e:
            pass                
        try:    
            ds1 = xr.concat(ds_list_2, 
                            dim='number')
        except Exception as e:
            pass                
        try:            
            ds2 = xr.concat(ds_list_3, 
                            dim='number')
        except Exception as e:
            pass                
        try:            
            ds3 = xr.concat(ds_list_4, 
                            dim='number')
        except Exception as e:
            pass                
        try:            
            ds4 = xr.concat(ds_list_5, 
                            dim='number')
        except Exception as e:
            pass                
        try:            
            ds5 = xr.concat(ds_list_6, 
                            dim='number')
        except Exception as e:
            pass                
        try:            
            ds6 = xr.concat(ds_list_7, 
                            dim='number')
        except Exception as e:
            pass                
        try:            
            ds7 = xr.concat(ds_list_8, 
                            dim='number')
        except Exception as e:
            pass                
        try:            
            ds8 = xr.concat(ds_list_9, 
                            dim='number')
        except Exception as e:
            pass                
        try:            
            ds9 = xr.concat(ds_list_10, 
                            dim='number')
        except Exception as e:
            pass                
        try:            
            ds10 = xr.concat(ds_list_11, 
                             dim='number') 
        except Exception as e:
            pass    
        
        try:            
            ds11 = xr.concat(ds_list_12, 
                             dim='number') 
        except Exception as e:
            pass    
        
        try:            
            ds12 = xr.concat(ds_list_13, 
                             dim='number') 
        except Exception as e:
            pass  
        
        try:            
            ds13 = xr.concat(ds_list_14, 
                             dim='number') 
        except Exception as e:
            pass  
        
        farther = False
        try:
            ds
        except Exception as e:
            try:
                ds = ds1
            except Exception as e:
                try:
                    ds = ds2
                except Exception as e:
                    try:
                        ds = ds3
                    except Exception as e:
                        try:
                            ds = ds4
                        except Exception as e:
                            try:
                                ds = ds5
                            except Exception as e:
                                try:
                                    ds = ds6
                                except Exception as e:
                                    farther = True
                                    
        if farther == True:
            try:
                ds = ds7
            except Exception as e:
                try:
                    ds = ds8
                except Exception as e:
                    try:
                        ds = ds9
                    except Exception as e:
                        try:
                            ds = ds10
                        except Exception as e:
                            try:
                                ds = ds11
                            except Exception as e:
                                try:
                                    ds = ds12
                                except Exception as e:
                                    try:
                                        ds = ds13
                                    except Exception as e:
                                        pass
        else:
            pass                                                            
        
    else:
        
        file_pattern = file_paths_for_xarray(paths)
        
        try:
            ds = xr.open_mfdataset(file_pattern, 
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False, 
                                filter_by_keys={'typeOfLevel': 'surface'})
            ds = shift_longitude(ds)
        except Exception as e:
            pass

        try:        
            ds1 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'meanSea'})
            ds1 = shift_longitude(ds1)
        except Exception as e:
            pass

        try: 
            ds2 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'depthBelowLandLayer'})
            ds2 = shift_longitude(ds2)
        except Exception as e:
            pass
        try: 
            ds3 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'heightAboveGround'})
            ds3 = shift_longitude(ds3)
        except Exception as e:
            pass
        try: 
            ds4 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False,
                                    filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'10u'})
            ds4 = shift_longitude(ds4)
        except Exception as e:
            pass
        
        try: 
            ds5 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'10v'})
            ds5 = shift_longitude(ds5)
        except Exception as e:
            pass
        
        try: 
            ds6 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'atmosphereSingleLayer'})
            ds6 = shift_longitude(ds6)
        except Exception as e:
            pass            
        try: 
            ds7 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested',
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'})
            ds7 = shift_longitude(ds7)
        except Exception as e:
            pass
        try: 
            ds8 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
            ds8 = shift_longitude(ds8)
        except Exception as e:
            pass
        try: 
            ds9 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'t'})
            ds9 = shift_longitude(ds9)
        except Exception as e:
            pass
        try: 
            ds10 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'r'})
            ds10 = shift_longitude(ds10)
        except Exception as e:
            pass
        try: 
            ds11 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested',
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'u'})
            ds11 = shift_longitude(ds11)
        except Exception as e:
            pass
        try: 
            ds12 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'v'})
            ds12 = shift_longitude(ds12)
        except Exception as e:
            pass     
        
        try: 
            ds13 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False,
                                    filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer'})
            ds13 = shift_longitude(ds13)
        except Exception as e:
            pass       
        
    try: 
        ds['surface_pressure'] = ds['sp']
        ds = ds.drop_vars('sp')
    except Exception as e:
        pass    
    
    try: 
        ds['total_precipitation'] = ds['tp']
        ds = ds.drop_vars('tp')
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_snow'] = ds['csnow']
        ds = ds.drop_vars('csnow')
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_ice_pellets'] = ds['cicep']
        ds = ds.drop_vars('cicep')
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_freezing_rain'] = ds['cfrzr']
        ds = ds.drop_vars('cfrzr')
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_rain'] = ds['crain']
        ds = ds.drop_vars('crain')
    except Exception as e:
        pass  
    
    try:     
        ds['time_mean_surface_latent_heat_flux'] = ds['avg_slhtf']
        ds = ds.drop_vars('avg_slhtf')
    except Exception as e:
        pass  
      
    try:     
        ds['time_mean_surface_sensible_heat_flux'] = ds['avg_ishf']
        ds = ds.drop_vars('avg_ishf')
    except Exception as e:
        pass   
    
    try:     
        ds['surface_downward_shortwave_radiation_flux'] = ds['sdswrf']
        ds = ds.drop_vars('sdswrf')
    except Exception as e:
        pass    
    
    try:     
        ds['surface_downward_longwave_radiation_flux'] = ds['sdlwrf']
        ds = ds.drop_vars('sdlwrf')
    except Exception as e:
        pass    
    
    try:     
        ds['surface_upward_shortwave_radiation_flux'] = ds['suswrf']
        ds = ds.drop_vars('suswrf')
    except Exception as e:
        pass    
    
    try:     
        ds['surface_upward_longwave_radiation_flux'] = ds['sulwrf']
        ds = ds.drop_vars('sulwrf')
    except Exception as e:
        pass    

    try:
        ds['orography'] = ds['orog']
        ds = ds.drop_vars('orog')
    except Exception as e:
        pass
    
    try:     
        ds['water_equivalent_of_accumulated_snow_depth'] = ds['sdwe']
        ds = ds.drop_vars('sdwe')
    except Exception as e:
        pass   
    
    try:     
        ds['snow_depth'] = ds['sde']
        ds = ds.drop_vars('sde')
    except Exception as e:
        pass    
    
    try:     
        ds['sea_ice_thickness'] = ds['sithick']
        ds = ds.drop_vars('sithick')
    except Exception as e:
        pass     
    
    try:        
        ds['surface_visibility'] = ds['vis']
        ds = ds.drop_vars('vis')
    except Exception as e:
        pass       
    
    try:        
        ds['surface_wind_gust'] = ds['gust']
        ds = ds.drop_vars('gust')
    except Exception as e:
        pass   
    
    try:        
        ds['percent_frozen_precipitation'] = ds['cpofp']
        ds = ds.drop_vars('cpofp')
    except Exception as e:
        pass   
    
    try:        
        ds['surface_cape'] = ds['cape']
        ds = ds.drop_vars('cape')
    except Exception as e:
        pass        
    try:        
        ds['surface_cin'] = ds['cin']
        ds = ds.drop_vars('cin')
    except Exception as e:
        pass 
    
    try:     
        ds['mslp'] = ds1['prmsl']
    except Exception as e:
        pass           
    try:        
        ds['soil_temperature'] = ds2['st']
    except Exception as e:
        pass
       
    try:        
        ds['volumetric_soil_moisture_content'] = ds2['soilw']
    except Exception as e:
        pass
    
    try:     
        ds['2m_temperature'] = ds3['t2m']
    except Exception as e:
        pass 
    
    try:
        ds['2m_relative_humidity'] = ds3['r2']
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point'] = ds3['d2m']
    except Exception as e:
        pass
    
    try:
        ds['maximum_temperature'] = ds3['tmax']
    except Exception as e:
        pass
    
    try:
        ds['minimum_temperature'] = ds3['tmin']
    except Exception as e:
        pass
    
    try:
        ds['10m_u_wind_component'] = ds4['u10']
    except Exception as e:
        pass

    try:
        ds['10m_v_wind_component'] = ds5['v10']
    except Exception as e:
        pass
    
    try:
        ds['precipitable_water'] = ds6['pwat']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_cape'] = ds7['cape']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_cin'] = ds7['cin']
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height'] = ds8['gh']
    except Exception as e:
        pass
    
    try:
        ds['air_temperature'] = ds9['t']
    except Exception as e:
        pass
    try:
        ds['relative_humidity'] = ds10['r']
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component'] = ds11['u']
    except Exception as e:
        pass

    try:
        ds['v_wind_component'] = ds12['v']
    except Exception as e:
        pass
    
    try:
        ds['3km_helicity'] = ds13['hlcy']
    except Exception as e:
        pass
    
    clear_gefs_idx_files(paths)
    
    return ds


def secondary_gefs_post_processing(paths):
    
    
    """
    This function post-processes the GEFS (Secondary) Parameters for GEFS0P50 and GEFS0P25. 
    
    Required Arguments: 
    
    1) 1) paths (List) - A list of file paths to the GEFS0P50 Secondary Parameters. 
    
    Returns
    -------
    
    An xarray data array of the post-processed GEFS data. 
    GRIB Keys are converted to Plain Language Keys. 
    
    New Variable Keys After Post-Processing (Decrypted GRIB Keys Into Plain Language)
    --------------------------------------------------------------------------------
    
        'surface_temperature'
        'surface_visibility'
        'surface_wind_gust'
        'haines_index'
        'plant_canopy_surface_water'
        'snow_cover'
        'percent_frozen_precipitation'
        'snow_phase_change_heat_flux'
        'surface_roughness'
        'frictional_velocity'
        'wilting_point'
        'field_capacity'
        'sunshine_duration'
        'surface_lifted_index'
        'best_4_layer_lifted_index'
        'land_sea_mask'
        'sea_ice_area_fraction'
        'orography'
        'surface_cape'
        'surface_cin'
        'convective_precipitation_rate'
        'precipitation_rate'
        'total_convective_precipitation'
        'total_non_convective_precipitation'
        'total_precipitation'
        'water_runoff'
        'ground_heat_flux'
        'time_mean_u_component_of_atmospheric_surface_momentum_flux'
        'time_mean_v_component_of_atmospheric_surface_momentum_flux'
        'instantaneous_eastward_gravity_wave_surface_flux'
        'instantaneous_northward_gravity_wave_surface_flux'
        'uv_b_downward_solar_flux'
        'clear_sky_uv_b_downward_solar_flux'
        'average_surface_albedo'
        'mslp'
        'mslp_eta_reduction'
        'boundary_layer_u_wind_component'
        'boundary_layer_v_wind_component'
        'ventilation_rate' 
        'geopotential_height'
        'air_temperature' 
        'vertical_velocity'
        'u_wind_component'
        'v_wind_component'
        'ozone_mixing_ratio'
        'absolute_vorticity'
        'cloud_mixing_ratio'
        'icing_severity'
        'total_cloud_cover'
        'relative_humidity'
        'liquid_volumetric_soil_moisture_non_frozen'
        'soil_temperature'
        'volumetric_soil_moisture_content'
        '2m_specific_humidity'
        '2m_dew_point'
        '2m_apparent_temperature'
        '80m_specific_humidity'
        '80m_air_pressure'
        '80m_u_wind_component'
        '80m_v_wind_component'
        'atmosphere_single_layer_relative_humidity'
        'cloud_water'
        'total_ozone'
        'cloud_ceiling_height'
        'brightness_temperature'
        '3km_helicity'
        'u_component_of_storm_motion'
        'v_component_of_storm_motion'
        'tropopause_height'
        'tropopause_pressure'
        'tropopause_standard_atmosphere_reference_height'
        'tropopause_u_wind_component'
        'tropopause_v_wind_component'
        'tropopause_temperature'
        'tropopause_vertical_speed_shear'
        'max_wind_u_component'
        'max_wind_v_component'
        'zero_deg_c_isotherm_geopotential_height'
        'zero_deg_c_isotherm_relative_humidity'
        'highest_tropospheric_freezing_level_geopotential_height'
        'highest_tropospheric_freezing_level_relative_humidity'
        '995_sigma_relative_humdity'
        '995_sigma_temperature'
        '995_sigma_theta'
        '995_u_wind_component'
        '995_v_wind_component'
        '995_vertical_velocity'
        'potential_vorticity'
        'theta_level_u_wind_component'
        'theta_level_v_wind_component'
        'theta_level_temperature'
        'theta_level_montgomery_potential'
        'potential_vorticity_level_u_wind_component'
        'potential_vorticity_level_v_wind_component'
        'potential_vorticity_level_temperature'
        'potential_vorticity_level_geopotential_height'
        'potential_vorticity_level_air_pressure'
        'potential_vorticity_level_vertical_speed_shear'
        'mixed_layer_air_temperature'
        'mixed_layer_relative_humidity'
        'mixed_layer_specific_humidity'
        'mixed_layer_u_wind_component'
        'mixed_layer_v_wind_component'
        'mixed_layer_dew_point'
        'mixed_layer_precipitable_water'
        'parcel_lifted_index_to_500hPa'
        'mixed_layer_cape'
        'mixed_layer_cin'
        'pressure_level_from_which_a_parcel_was_lifted' 
    
    """

    
            
    clear_gefs_idx_files(paths)

    if len(paths) == 1:
        
        file_pattern = file_paths_for_xarray(paths)
        
        try:
            ds = xr.open_mfdataset(file_pattern, 
                                   concat_dim='step', 
                                   combine='nested', 
                                   coords='minimal', 
                                   engine='cfgrib', 
                                   compat='override',
                                   decode_timedelta=False,
                                   filter_by_keys={'typeOfLevel': 'surface'})
            ds = shift_longitude(ds)
        except Exception as e:
            pass    
        try:        
            ds1 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False,
                                    filter_by_keys={'typeOfLevel': 'meanSea'})
            ds1 = shift_longitude(ds1) 
        except Exception as e:
            pass        
        try:        
            ds2 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal',
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'planetaryBoundaryLayer'})
            ds2 = shift_longitude(ds2)
        except Exception as e:
            pass          
        try:        
            ds3 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step',
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False,
                                    filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
            ds3 = shift_longitude(ds3)  
        except Exception as e:
            pass        
        try:        
            ds4 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step',
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'t'})
            ds4 = shift_longitude(ds4)
        except Exception as e:
            pass                    
        try:        
            ds5 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override',
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'w'})
            ds5 = shift_longitude(ds5)
        except Exception as e:
            pass        
        try:        
            ds6 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested',
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'u'})
            ds6 = shift_longitude(ds6)
        except Exception as e:
            pass        
        try:        
            ds7 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step',
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'v'})
            ds7 = shift_longitude(ds7)
        except Exception as e:
            pass        
        try:        
            ds8 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override',
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'o3mr'})
            ds8 = shift_longitude(ds8)
        except Exception as e:
            pass        
        try:        
            ds9 = xr.open_mfdataset(file_pattern, 
                                    concat_dim='step', 
                                    combine='nested', 
                                    coords='minimal', 
                                    engine='cfgrib', 
                                    compat='override', 
                                    decode_timedelta=False, 
                                    filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'absv'})
            ds9 = shift_longitude(ds9)
        except Exception as e:
            pass        
        try:        
            ds10 = xr.open_mfdataset(file_pattern,
                                     concat_dim='step', 
                                     combine='nested', 
                                     coords='minimal',
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False,
                                     filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'clwmr'})
            ds10 = shift_longitude(ds10)
        except Exception as e:
            pass        
        try:        
            ds12 = xr.open_mfdataset(file_pattern,
                                     concat_dim='step',
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'ICSEV'})
            ds12 = shift_longitude(ds12)
        except Exception as e:
            pass        
        try:        
            ds13 = xr.open_mfdataset(file_pattern,
                                     concat_dim='step', 
                                     combine='nested', 
                                     coords='minimal',
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'tcc'})
            ds13 = shift_longitude(ds13)
        except Exception as e:
            pass        
        try:        
            ds14 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False,
                                     filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'r'})
            ds14 = shift_longitude(ds14) 
        except Exception as e:
            pass        
        try:        
            ds15 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested',
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'depthBelowLandLayer'})
            ds15 = shift_longitude(ds15)
        except Exception as e:
            pass        
        try:        
            ds16 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step', 
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'depthBelowLandLayer', 'shortName':'st'})
            ds16 = shift_longitude(ds16)
        except Exception as e:
            pass        
        try:        
            ds17 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step', 
                                     combine='nested',
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'depthBelowLandLayer', 'shortName':'soilw'})
            ds17 = shift_longitude(ds17)
        except Exception as e:
            pass        
        try:        
            ds18 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step', 
                                     combine='nested',
                                     coords='minimal', 
                                     engine='cfgrib',
                                     compat='override',
                                     decode_timedelta=False,
                                     filter_by_keys={'typeOfLevel': 'heightAboveGround'})
            ds18 = shift_longitude(ds18)
        except Exception as e:
            pass        
        try:        
            ds19 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'q'})
            ds19 = shift_longitude(ds19)
        except Exception as e:
            pass        
        try:        
            ds20 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step', 
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'t'})
            ds20 = shift_longitude(ds20)
        except Exception as e:
            pass        
        try:        
            ds21 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step', 
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'pres'})
            ds21 = shift_longitude(ds21)
        except Exception as e:
            pass        
        try:        
            ds22 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step', 
                                     combine='nested',
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False,
                                     filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'u'})
            ds22= shift_longitude(ds22)
        except Exception as e:
            pass        
        try:        
            ds23 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested',
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'v'})
            ds23 = shift_longitude(ds23)
        except Exception as e:
            pass        
        try:        
            ds24 = xr.open_mfdataset(file_pattern,
                                     concat_dim='step', 
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False,
                                     filter_by_keys={'typeOfLevel': 'atmosphereSingleLayer'})
            ds24 = shift_longitude(ds24)
        except Exception as e:
            pass        
        try:        
            ds25 = xr.open_mfdataset(file_pattern,
                                     concat_dim='step',
                                     combine='nested',
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False,
                                     filter_by_keys={'typeOfLevel': 'cloudCeiling'})
            ds25 = shift_longitude(ds25)
        except Exception as e:
            pass        
        try:        
            ds26 = xr.open_mfdataset(file_pattern,
                                     concat_dim='step',
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'nominalTop'})
            ds26 = shift_longitude(ds26)
        except Exception as e:
            pass        
        try:        
            ds27 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib',
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer'})
            ds27 = shift_longitude(ds27)
        except Exception as e:
            pass        
        try:        
            ds28 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested',
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer', 'shortName':'ustm'})
            ds28 = shift_longitude(ds28)
        except Exception as e:
            pass        
        try:        
            ds29 = xr.open_mfdataset(file_pattern,
                                     concat_dim='step',
                                     combine='nested', 
                                     coords='minimal',
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer', 'shortName':'vstm'})
            ds29 = shift_longitude(ds29)
        except Exception as e:
            pass        
        try:        
            ds30 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested',
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'tropopause'})
            ds30 = shift_longitude(ds30)
        except Exception as e:
            pass        
        try:        
            ds31 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'maxWind'})
            ds31 = shift_longitude(ds31)
        except Exception as e:
            pass        
        try:        
            ds32 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested',
                                     coords='minimal',
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'isothermZero'})
            ds32 = shift_longitude(ds32)
        except Exception as e:
            pass        
        try:        
            ds33 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override',
                                     decode_timedelta=False,
                                     filter_by_keys={'typeOfLevel': 'highestTroposphericFreezing'})
            ds33 = shift_longitude(ds33)
        except Exception as e:
            pass        
        try:        
            ds34 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested',
                                     coords='minimal',
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'sigmaLayer'})
            ds34 = shift_longitude(ds33)
        except Exception as e:
            pass        
        try:        
            ds35 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested',
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'sigma'})
            ds35 = shift_longitude(ds35)
        except Exception as e:
            pass        
        try:        
            ds36 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested',
                                     coords='minimal',
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False,
                                     filter_by_keys={'typeOfLevel': 'theta'})
            ds36 = shift_longitude(ds36)
        except Exception as e:
            pass        
        try:        
            ds37 = xr.open_mfdataset(file_pattern,
                                     concat_dim='step', 
                                     combine='nested',
                                     coords='minimal', 
                                     engine='cfgrib',
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'theta', 'shortName':'u'})
            ds37 = shift_longitude(ds37)
        except Exception as e:
            pass        
        try:        
            ds38 = xr.open_mfdataset(file_pattern,
                                     concat_dim='step',
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'theta', 'shortName':'v'})
            ds38 = shift_longitude(ds38)
        except Exception as e:
            pass        
        try:        
            ds39 = xr.open_mfdataset(file_pattern,
                                     concat_dim='step', 
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib',
                                     compat='override',
                                     decode_timedelta=False,
                                     filter_by_keys={'typeOfLevel': 'theta', 'shortName':'t'})
            ds39 = shift_longitude(ds39)
        except Exception as e:
            pass        
        try:        
            ds40 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested',
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False,
                                     filter_by_keys={'typeOfLevel': 'theta', 'shortName':'mont'})
            ds40 = shift_longitude(ds40)
        except Exception as e:
            pass        
        try:        
            ds41 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'potentialVorticity'})
            ds41 = shift_longitude(ds41)
        except Exception as e:
            pass        
        try:        
            ds42 = xr.open_mfdataset(file_pattern,
                                     concat_dim='step', 
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override',
                                     decode_timedelta=False,
                                     filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'})
            ds42 = shift_longitude(ds42)
        except Exception as e:
            pass        
        try:        
            ds43 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'dpt'})
            ds43 = shift_longitude(ds43)
        except Exception as e:
            pass        
        try:        
            ds44 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False,
                                     filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'pwat'})
            ds44 = shift_longitude(ds44)
        except Exception as e:
            pass        
        try:        
            ds45 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step', 
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False,
                                     filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'pli'})
            ds45 = shift_longitude(ds45)
        except Exception as e:
            pass        
        try:        
            ds46 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step',
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'cape'})
            ds46 = shift_longitude(ds46)
        except Exception as e:
            pass        
        try:        
            ds47 = xr.open_mfdataset(file_pattern,
                                     concat_dim='step', 
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib', 
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'cin'})
            ds47 = shift_longitude(ds47)
        except Exception as e:
            pass        
        try:        
            ds48 = xr.open_mfdataset(file_pattern, 
                                     concat_dim='step', 
                                     combine='nested', 
                                     coords='minimal', 
                                     engine='cfgrib',
                                     compat='override', 
                                     decode_timedelta=False, 
                                     filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'plpl'})
            ds48 = shift_longitude(ds48)
        except Exception as e:
            pass        
        
    else:
        
        clear_gefs_idx_files(paths)

        paths = file_paths_for_xarray(paths)
        try:
            ds_list_1 = []      
            for path in paths:
                file_pattern = path
                ds = xr.open_mfdataset(file_pattern, 
                                       concat_dim='step',
                                       combine='nested',
                                       coords='minimal', 
                                       engine='cfgrib', 
                                       compat='override', 
                                       decode_timedelta=False,
                                       filter_by_keys={'typeOfLevel': 'surface'})
                ds = shift_longitude(ds)
                ds_list_1.append(ds)
        except Exception as e:
            pass           
        try:
            ds_list_2 = []
            for path in paths:
                file_pattern = path
                ds1 = xr.open_mfdataset(file_pattern,
                                        concat_dim='step',
                                        combine='nested',
                                        coords='minimal',
                                        engine='cfgrib', 
                                        compat='override',
                                        decode_timedelta=False,
                                        filter_by_keys={'typeOfLevel': 'meanSea'})
                ds1 = shift_longitude(ds1) 
                ds_list_2.append(ds1)
        except Exception as e:
            pass                   
        try:
            ds_list_3 = []
            for path in paths:
                file_pattern = path
                ds2 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step',
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False,
                                        filter_by_keys={'typeOfLevel': 'planetaryBoundaryLayer'})
                ds2 = shift_longitude(ds2)
                ds_list_3.append(ds2)
        except Exception as e:
            pass           
        try:
            ds_list_4 = []
            for path in paths:
                file_pattern = path
                ds3 = xr.open_mfdataset(file_pattern,
                                        concat_dim='step',
                                        combine='nested',
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override',
                                        decode_timedelta=False, 
                                        filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
                ds3 = shift_longitude(ds3)
                ds_list_4.append(ds3)  
        except Exception as e:
            pass           
        try:
            ds_list_5 = []
            for path in paths:
                file_pattern = path
                ds4 = xr.open_mfdataset(file_pattern,
                                        concat_dim='step', 
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False,
                                        filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'t'})
                ds4 = shift_longitude(ds4)
                ds_list_5.append(ds4)
        except Exception as e:
            pass           
        try:            
            ds_list_6 = []
            for path in paths:
                file_pattern = path
                ds5 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step', 
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False, 
                                        filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'w'})
                ds5 = shift_longitude(ds5)
                ds_list_6.append(ds5)
        except Exception as e:
            pass           
        try:
            ds_list_7 = []
            for path in paths:
                file_pattern = path
                ds6 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step',
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False, 
                                        filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'u'})
                ds6 = shift_longitude(ds6)
                ds_list_7.append(ds6)  
        except Exception as e:
            pass           
        try:
            ds_list_8 = []
            for path in paths:
                file_pattern = path
                ds7 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step',
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False,
                                        filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'v'})
                ds7 = shift_longitude(ds7)
                ds_list_8.append(ds7)
        except Exception as e:
            pass           
        try:
            ds_list_9 = []
            for path in paths:
                file_pattern = path
                ds8 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step',
                                        combine='nested', 
                                        coords='minimal',
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False,
                                        filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'o3mr'})
                ds8 = shift_longitude(ds8)
                ds_list_9.append(ds8) 
        except Exception as e:
            pass           
        try:
            ds_list_10 = []
            for path in paths:
                file_pattern = path
                ds9 = xr.open_mfdataset(file_pattern, 
                                        concat_dim='step',
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False,
                                        filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'absv'})
                ds9 = shift_longitude(ds9)
                ds_list_10.append(ds9)
        except Exception as e:
            pass           
        try:
            ds_list_11 = []
            for path in paths:
                file_pattern = path
                ds10 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'clwmr'})
                ds10 = shift_longitude(ds10)
                ds_list_11.append(ds10)  
        except Exception as e:
            pass           
        try:
            ds_list_12 = []
            for path in paths:
                file_pattern = path
                ds12 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'ICSEV'})
                ds12 = shift_longitude(ds12)
                ds_list_12.append(ds12) 
        except Exception as e:
            pass           
        try:
            ds_list_13 = []
            for path in paths:
                file_pattern = path
                ds13 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal', 
                                         engine='cfgrib',
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'tcc'})
                ds13 = shift_longitude(ds13)
                ds_list_13.append(ds13)
        except Exception as e:
            pass           
        try:
            ds_list_14 = []
            for path in paths:
                file_pattern = path
                ds14 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal',
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'r'})
                ds14 = shift_longitude(ds14)
                ds_list_14.append(ds14)
        except Exception as e:
            pass           
        try:
            ds_list_15 = []
            for path in paths:
                file_pattern = path
                ds15 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal',
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'depthBelowLandLayer'})
                ds15 = shift_longitude(ds15)
                ds_list_15.append(ds15) 
        except Exception as e:
            pass           
        try:
            ds_list_16 = []
            for path in paths:
                file_pattern = path
                ds16 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step', 
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'depthBelowLandLayer', 'shortName':'st'})
                ds16 = shift_longitude(ds16)
                ds_list_16.append(ds16)
        except Exception as e:
            pass           
        try:
            ds_list_17 = []
            for path in paths:
                file_pattern = path
                ds17 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step', 
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'depthBelowLandLayer', 'shortName':'soilw'})
                ds17 = shift_longitude(ds17)
                ds_list_17.append(ds17)
        except Exception as e:
            pass           
        try:
            ds_list_18 = []
            for path in paths:
                file_pattern = path
                ds18 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step', 
                                         combine='nested',
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'heightAboveGround'})
                ds18 = shift_longitude(ds18)
                ds_list_18.append(ds18)
        except Exception as e:
            pass           
        try:
            ds_list_19 = []
            for path in paths:
                file_pattern = path
                ds19 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib',
                                         compat='override',
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'q'})
                ds19 = shift_longitude(ds19)
                ds_list_19.append(ds19)                
        except Exception as e:
            pass           
        try:
            ds_list_20 = []
            for path in paths:
                file_pattern = path
                ds20 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal',
                                         engine='cfgrib',
                                         compat='override',
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'t'})
                ds20 = shift_longitude(ds20)
                ds_list_20.append(ds20)            
        except Exception as e:
            pass           
        try:
            ds_list_21 = []
            for path in paths:
                file_pattern = path
                ds21 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'pres'})
                ds21 = shift_longitude(ds21) 
                ds_list_21.append(ds21)            
        except Exception as e:
            pass           
        try:
            ds_list_22 = []
            for path in paths:
                file_pattern = path
                ds22 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'u'})
                ds22 = shift_longitude(ds22)
                ds_list_22.append(ds22)            
        except Exception as e:
            pass           
        try:
            ds_list_23 = []
            for path in paths:
                file_pattern = path
                ds23 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal',
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'v'})
                ds23 = shift_longitude(ds23)
                ds_list_23.append(ds23)            
        except Exception as e:
            pass           
        try:
            ds_list_24 = []
            for path in paths:
                file_pattern = path
                ds24 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'atmosphereSingleLayer'})
                ds24 = shift_longitude(ds24)
                ds_list_24.append(ds24)
        except Exception as e:
            pass   
        try:
            ds_list_25= []
            for path in paths:
                file_pattern = path
                ds25 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step', 
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'cloudCeiling'})
                ds25 = shift_longitude(ds25)
                ds_list_25.append(ds25)            
        except Exception as e:
            pass           
        try:
            ds_list_26 = []
            for path in paths:
                file_pattern = path
                ds26 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal',
                                         engine='cfgrib',
                                         compat='override',
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'nominalTop'})
                ds26 = shift_longitude(ds26)
                ds_list_26.append(ds26)            
        except Exception as e:
            pass           
        try:
            ds_list_27 = []
            for path in paths:
                file_pattern = path
                ds27 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal',
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer'})
                ds27 = shift_longitude(ds27)
                ds_list_27.append(ds27)            
        except Exception as e:
            pass           
        try:
            ds_list_28 = []
            for path in paths:
                file_pattern = path
                ds28 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal',
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer', 'shortName':'ustm'})
                ds28 = shift_longitude(ds28)
                ds_list_28.append(ds28)            
        except Exception as e:
            pass           
        try:
            ds_list_29 = []
            for path in paths:
                file_pattern = path
                ds29 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer', 'shortName':'vstm'})
                ds29 = shift_longitude(ds29) 
                ds_list_29.append(ds29)            
        except Exception as e:
            pass           
        try:
            ds_list_30 = []
            for path in paths:
                file_pattern = path
                ds30 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'tropopause'})
                ds30 = shift_longitude(ds30)
                ds_list_30.append(ds30)
        except Exception as e:
            pass   
        try:
            ds_list_31 = []
            for path in paths:
                file_pattern = path
                ds31 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal',
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'maxWind'})
                ds31 = shift_longitude(ds31)
                ds_list_31.append(ds31)
        except Exception as e:
            pass           
        try:
            ds_list_32 = []
            for path in paths:
                file_pattern = path
                ds32 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'isothermZero'})
                ds32 = shift_longitude(ds32)
                ds_list_32.append(ds32)
        except Exception as e:
            pass   
        try:
            ds_list_33 = []
            for path in paths:
                file_pattern = path
                ds33 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'highestTroposphericFreezing'})
                ds33 = shift_longitude(ds33)
                ds_list_33.append(ds33)  
        except Exception as e:
            pass           
        try:
            ds_list_34 = []
            for path in paths:
                file_pattern = path
                ds34 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step', 
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib',
                                         compat='override', 
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'sigmaLayer'})
                ds34 = shift_longitude(ds33)
                ds_list_34.append(ds34)            
        except Exception as e:
            pass           
        try:
            ds_list_35 = []
            for path in paths:
                file_pattern = path
                ds35 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'sigma'})
                ds35 = shift_longitude(ds35)
                ds_list_35.append(ds35)
        except Exception as e:
            pass           
        try:
            ds_list_36 = []
            for path in paths:
                file_pattern = path
                ds36 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'theta'})
                ds36 = shift_longitude(ds36)
                ds_list_36.append(ds36)            
        except Exception as e:
            pass           
        try:
            ds_list_37 = []
            for path in paths:
                file_pattern = path
                ds37 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'theta', 'shortName':'u'})
                ds37 = shift_longitude(ds37)
                ds_list_37.append(ds37)            
        except Exception as e:
            pass           
        try:
            ds_list_38 = []
            for path in paths:
                file_pattern = path
                ds38 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal', 
                                         engine='cfgrib',
                                         compat='override',
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'theta', 'shortName':'v'})
                ds38 = shift_longitude(ds38)
                ds_list_38.append(ds38)            
        except Exception as e:
            pass           
        try:
            ds_list_39 = []
            for path in paths:
                file_pattern = path
                ds39 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step', 
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'theta', 'shortName':'t'})
                ds39 = shift_longitude(ds39)
                ds_list_39.append(ds39)            
        except Exception as e:
            pass           
        try:
            ds_list_40 = []
            for path in paths:
                file_pattern = path
                ds40 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'theta', 'shortName':'mont'})
                ds40 = shift_longitude(ds40)
                ds_list_40.append(ds40)            
        except Exception as e:
            pass           
        try:
            ds_list_41 = []
            for path in paths:
                file_pattern = path
                ds41 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'potentialVorticity'})
                ds41 = shift_longitude(ds41)
                ds_list_41.append(ds41)
        except Exception as e:
            pass           
        try:
            ds_list_42 = []
            for path in paths:
                file_pattern = path
                ds42 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'})
                ds42 = shift_longitude(ds42)
                ds_list_42.append(ds42)
        except Exception as e:
            pass           
        try:
            ds_list_43 = []
            for path in paths:
                file_pattern = path
                ds43 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal',
                                         engine='cfgrib',
                                         compat='override',
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'dpt'})
                ds43 = shift_longitude(ds43)
                ds_list_43.append(ds43)            
        except Exception as e:
            pass           
        try:
            ds_list_44 = []
            for path in paths:
                file_pattern = path
                ds44 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'pwat'})
                ds44 = shift_longitude(ds44)
                ds_list_44.append(ds44)            
        except Exception as e:
            pass           
        try:
            ds_list_45 = []
            for path in paths:
                file_pattern = path
                ds45 = xr.open_mfdataset(file_pattern, 
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'pli'})
                ds45 = shift_longitude(ds45)
                ds_list_45.append(ds45)            
        except Exception as e:
            pass           
        try:
            ds_list_46 = []
            for path in paths:
                file_pattern = path
                ds46 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal',
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'cape'})
                ds46 = shift_longitude(ds46)
                ds_list_46.append(ds46)            
        except Exception as e:
            pass           
        try:
            ds_list_47 = []
            for path in paths:
                file_pattern = path
                ds47 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested', 
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override',
                                         decode_timedelta=False,
                                         filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'cin'})
                ds47 = shift_longitude(ds47)
                ds_list_47.append(ds47)            
        except Exception as e:
            pass           
        try:
            ds_list_48 = []
            for path in paths:
                file_pattern = path
                ds48 = xr.open_mfdataset(file_pattern,
                                         concat_dim='step',
                                         combine='nested',
                                         coords='minimal', 
                                         engine='cfgrib', 
                                         compat='override', 
                                         decode_timedelta=False, 
                                         filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'shortName':'plpl'})
                ds48 = shift_longitude(ds48)
                ds_list_48.append(ds48) 
        except Exception as e:
            pass           
    
        try:    
            ds = xr.concat(ds_list_1,
                           dim='number')
        except Exception as e:
            pass               
        try:            
            ds1 = xr.concat(ds_list_2,
                            dim='number')
        except Exception as e:
            pass               
        try:            
            ds2 = xr.concat(ds_list_3,
                            dim='number')
        except Exception as e:
            pass               
        try:            
            ds3 = xr.concat(ds_list_4,
                            dim='number')
        except Exception as e:
            pass               
        try:            
            ds4 = xr.concat(ds_list_5,
                            dim='number')
        except Exception as e:
            pass               
        try:            
            ds5 = xr.concat(ds_list_6,
                            dim='number')
        except Exception as e:
            pass               
        try:            
            ds6 = xr.concat(ds_list_7,
                            dim='number')
        except Exception as e:
            pass               
        try:            
            ds7 = xr.concat(ds_list_8,
                            dim='number')
        except Exception as e:
            pass               
        try:            
            ds8 = xr.concat(ds_list_9,
                            dim='number')
        except Exception as e:
            pass               
        try:            
            ds9 = xr.concat(ds_list_10, 
                            dim='number')
        except Exception as e:
            pass               
        try:            
            ds10 = xr.concat(ds_list_11,
                             dim='number')
        except Exception as e:
            pass           
        try:        
            ds12 = xr.concat(ds_list_12,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds13 = xr.concat(ds_list_13, 
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds14 = xr.concat(ds_list_14, 
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds15 = xr.concat(ds_list_15,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds16 = xr.concat(ds_list_16,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds17 = xr.concat(ds_list_17,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds18 = xr.concat(ds_list_18, 
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds19 = xr.concat(ds_list_19, 
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds20 = xr.concat(ds_list_20,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds21 = xr.concat(ds_list_21, 
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds22 = xr.concat(ds_list_22, 
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds23 = xr.concat(ds_list_23,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds24 = xr.concat(ds_list_24,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds25 = xr.concat(ds_list_25,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds26 = xr.concat(ds_list_26,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds27 = xr.concat(ds_list_27,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds28 = xr.concat(ds_list_28,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds29 = xr.concat(ds_list_29,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds30 = xr.concat(ds_list_30,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds31 = xr.concat(ds_list_31,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds32 = xr.concat(ds_list_32,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds33 = xr.concat(ds_list_33,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds34 = xr.concat(ds_list_34, 
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds35 = xr.concat(ds_list_35, 
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds36 = xr.concat(ds_list_36,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds37 = xr.concat(ds_list_37,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds38 = xr.concat(ds_list_38,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds39 = xr.concat(ds_list_39,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds40 = xr.concat(ds_list_40, 
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds41 = xr.concat(ds_list_41, 
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds42 = xr.concat(ds_list_42, 
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds43 = xr.concat(ds_list_43,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds44 = xr.concat(ds_list_44, 
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds45 = xr.concat(ds_list_45,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds46 = xr.concat(ds_list_46,
                             dim='number')
        except Exception as e:
            pass               
        try:            
            ds47 = xr.concat(ds_list_47, 
                             dim='number')
        except Exception as e:
            pass               
        try:
            ds48 = xr.concat(ds_list_48,
                             dim='number')
        except Exception as e:
            pass                           
        
        
    try:
        ds['surface_temperature'] = ds['t']
        ds = ds.drop_vars('t')
    except Exception as e:
        pass
    try:        
        ds['surface_visibility'] = ds['vis']
        ds = ds.drop_vars('vis')
    except Exception as e:
        pass        
    try:        
        ds['surface_wind_gust'] = ds['gust']
        ds = ds.drop_vars('gust')
    except Exception as e:
        pass        
    try:        
        ds['haines_index'] = ds['hindex']
        ds = ds.drop_vars('hindex')
    except Exception as e:
        pass        
    try:        
        ds['plant_canopy_surface_water'] = ds['cnwat']
        ds = ds.drop_vars('cnwat')
    except Exception as e:
        pass        
    try:        
        ds['snow_cover'] = ds['snowc']
        ds = ds.drop_vars('snowc')
    except Exception as e:
        pass        
    try:        
        ds['percent_frozen_precipitation'] = ds['cpofp']
        ds = ds.drop_vars('cpofp')
    except Exception as e:
        pass        
    try:        
        ds['snow_phase_change_heat_flux'] = ds['snohf']
        ds = ds.drop_vars('snohf')
    except Exception as e:
        pass        
    try:        
        ds['surface_roughness'] = ds['fsr']
        ds = ds.drop_vars('fsr')
    except Exception as e:
        pass        
    try:        
        ds['frictional_velocity'] = ds['fricv']
        ds = ds.drop_vars('fricv')
    except Exception as e:
        pass        
    try:        
        ds['wilting_point'] = ds['wilt']
        ds = ds.drop_vars('wilt')
    except Exception as e:
        pass        
    try:        
        ds['field_capacity'] = ds['fldcp']
        ds = ds.drop_vars('fldcp')
    except Exception as e:
        pass        
    try:        
        ds['sunshine_duration'] = ds['SUNSD']
        ds = ds.drop_vars('SUNSD')
    except Exception as e:
        pass        
    try:        
        ds['surface_lifted_index'] = ds['lftx']
        ds = ds.drop_vars('lftx')
    except Exception as e:
        pass        
    try:        
        ds['best_4_layer_lifted_index'] = ds['lftx4']
        ds = ds.drop_vars('lftx4')
    except Exception as e:
        pass        
    try:        
        ds['land_sea_mask'] = ds['lsm']
        ds = ds.drop_vars('lsm')
    except Exception as e:
        pass        
    try:        
        ds['sea_ice_area_fraction'] = ds['siconc']
        ds = ds.drop_vars('siconc')
    except Exception as e:
        pass        
    try:        
        ds['orography'] = ds['orog']
        ds = ds.drop_vars('orog')
    except Exception as e:
        pass        
    try:        
        ds['surface_cape'] = ds['cape']
        ds = ds.drop_vars('cape')
    except Exception as e:
        pass        
    try:        
        ds['surface_cin'] = ds['cin']
        ds = ds.drop_vars('cin')
    except Exception as e:
        pass        
    try:        
        ds['convective_precipitation_rate'] = ds['cpr']
        ds = ds.drop_vars('cpr')
    except Exception as e:
        pass        
    try:        
        ds['precipitation_rate'] = ds['prate']
        ds = ds.drop_vars('prate')
    except Exception as e:
        pass        
    try:        
        ds['total_convective_precipitation'] = ds['acpcp']
        ds = ds.drop_vars('acpcp')
    except Exception as e:
        pass        
    try:        
        ds['total_non_convective_precipitation'] = ds['ncpcp']
        ds = ds.drop_vars('ncpcp')
    except Exception as e:
        pass        
    try:        
        ds['total_precipitation'] = ds['total_convective_precipitation'] + ds['total_non_convective_precipitation']
    except Exception as e:
        pass        
    try:        
        ds['water_runoff'] = ds['watr']
        ds = ds.drop_vars('watr')
    except Exception as e:
        pass        
    try:        
        ds['ground_heat_flux'] = ds['gflux']
        ds = ds.drop_vars('gflux')
    except Exception as e:
        pass        
    try:        
        ds['time_mean_u_component_of_atmospheric_surface_momentum_flux'] = ds['avg_utaua']
        ds = ds.drop_vars('avg_utaua')
    except Exception as e:
        pass        
    try:        
        ds['time_mean_v_component_of_atmospheric_surface_momentum_flux'] = ds['avg_vtaua']
        ds = ds.drop_vars('avg_vtaua')
    except Exception as e:
        pass        
    try:        
        ds['instantaneous_eastward_gravity_wave_surface_flux'] = ds['iegwss']
        ds = ds.drop_vars('iegwss')
    except Exception as e:
        pass        
    try:        
        ds['instantaneous_northward_gravity_wave_surface_flux'] = ds['ingwss']
        ds = ds.drop_vars('ingwss')
    except Exception as e:
        pass        
    try:        
        ds['uv_b_downward_solar_flux'] = ds['duvb']
        ds = ds.drop_vars('duvb')
    except Exception as e:
        pass        
    try:        
        ds['clear_sky_uv_b_downward_solar_flux'] = ds['cduvb']
        ds = ds.drop_vars('cduvb')
    except Exception as e:
        pass        
    try:        
        ds['average_surface_albedo'] = ds['avg_al']
        ds = ds.drop_vars('avg_al')
    except Exception as e:
        pass        
    try:        
        ds['mslp'] = ds1['msl']
    except Exception as e:
        pass        
    try:        
        ds['mslp_eta_reduction'] = ds1['mslet']  
    except Exception as e:
        pass        
    try:        
        ds['boundary_layer_u_wind_component'] = ds2['u']
    except Exception as e:
        pass        
    try:        
        ds['boundary_layer_v_wind_component'] = ds2['v']
    except Exception as e:
        pass        
    try:        
        ds['ventilation_rate'] = ds2['VRATE']   
    except Exception as e:
        pass        
    try:        
        ds['geopotential_height'] = ds3['gh']
    except Exception as e:
        pass        
    try:        
        ds['air_temperature'] = ds4['t']
    except Exception as e:
        pass        
    try:        
        ds['vertical_velocity'] = ds5['w']
    except Exception as e:
        pass        
    try:        
        ds['u_wind_component'] = ds6['u']
    except Exception as e:
        pass        
    try:        
        ds['v_wind_component'] = ds7['v'] 
    except Exception as e:
        pass        
    try:        
        ds['ozone_mixing_ratio'] = ds8['o3mr']
    except Exception as e:
        pass        
    try:        
        ds['absolute_vorticity'] = ds9['absv']
    except Exception as e:
        pass        
    try:        
        ds['cloud_mixing_ratio'] = ds10['clwmr']
    except Exception as e:
        pass        
    try:        
        ds['icing_severity'] = ds12['ICSEV']
    except Exception as e:
        pass        
    try:        
        ds['total_cloud_cover'] = ds13['tcc']
    except Exception as e:
        pass        
    try:        
        ds['relative_humidity'] = ds14['r']
    except Exception as e:
        pass        
    try:        
        ds['liquid_volumetric_soil_moisture_non_frozen'] = ds15['soill']
    except Exception as e:
        pass        
    try:        
        ds['soil_temperature'] = ds16['st']
    except Exception as e:
        pass        
    try:        
        ds['volumetric_soil_moisture_content'] = ds17['soilw']
    except Exception as e:
        pass        
    try:        
        ds['2m_specific_humidity'] = ds18['sh2']
    except Exception as e:
        pass        
    try:        
        ds['2m_dew_point'] = ds18['d2m']
    except Exception as e:
        pass        
    try:        
        ds['2m_apparent_temperature'] = ds18['aptmp']
    except Exception as e:
        pass        
    try:        
        ds['80m_specific_humidity'] = ds19['q']
    except Exception as e:
        pass        
    try:        
        ds['80m_and_100m_temperature'] = ds20['t']
    except Exception as e:
        pass        
    try:        
        ds['80m_air_pressure'] = ds21['pres']
    except Exception as e:
        pass        
    try:        
        ds['80m_u_wind_component'] = ds22['u']
    except Exception as e:
        pass        
    try:        
        ds['80m_v_wind_component'] = ds23['v']
    except Exception as e:
        pass        
    try:        
        ds['atmosphere_single_layer_relative_humidity'] = ds24['r']
    except Exception as e:
        pass        
    try:        
        ds['cloud_water'] = ds24['cwat']
    except Exception as e:
        pass        
    try:        
        ds['total_ozone'] = ds24['tozne']
    except Exception as e:
        pass        
    try:        
        ds['cloud_ceiling_height'] = ds25['gh']
    except Exception as e:
        pass        
    try:        
        ds['brightness_temperature'] = ds26['btmp']
    except Exception as e:
        pass        
    try:        
        ds['3km_helicity'] = ds27['hlcy'] 
    except Exception as e:
        pass        
    try:        
        ds['u_component_of_storm_motion'] = ds28['ustm']
    except Exception as e:
        pass        
    try:        
        ds['v_component_of_storm_motion'] = ds29['vstm']
    except Exception as e:
        pass        
    try:        
        ds['tropopause_height'] = ds30['gh']
    except Exception as e:
        pass        
    try:        
        ds['tropopause_pressure'] = ds30['trpp']
    except Exception as e:
        pass        
    try:        
        ds['tropopause_standard_atmosphere_reference_height'] = ds30['icaht']
    except Exception as e:
        pass        
    try:        
        ds['tropopause_u_wind_component'] = ds30['u']
    except Exception as e:
        pass        
    try:        
        ds['tropopause_v_wind_component'] = ds30['v']
    except Exception as e:
        pass              
    try:        
        ds['tropopause_temperature'] = ds30['t']
    except Exception as e:
        pass              
    try:        
        ds['tropopause_vertical_speed_shear'] = ds30['vwsh']
    except Exception as e:
        pass              
    try:        
        ds['max_wind_u_component'] = ds31['u']
    except Exception as e:
        pass              
    try:        
        ds['max_wind_v_component'] = ds31['v']
    except Exception as e:
        pass              
    try:        
        ds['zero_deg_c_isotherm_geopotential_height'] = ds32['gh']
    except Exception as e:
        pass              
    try:        
        ds['zero_deg_c_isotherm_relative_humidity'] = ds32['r']
    except Exception as e:
        pass              
    try:        
        ds['highest_tropospheric_freezing_level_geopotential_height'] = ds33['gh']
    except Exception as e:
        pass              
    try:        
        ds['highest_tropospheric_freezing_level_relative_humidity'] = ds33['r']
    except Exception as e:
        pass              
    try:        
        ds['relative_humdity_by_sigma_layer'] = ds34['r']
    except Exception as e:
        pass              
    try:        
        ds['995_sigma_relative_humdity'] = ds35['r']
    except Exception as e:
        pass              
    try:        
        ds['995_sigma_temperature'] = ds35['t']
    except Exception as e:
        pass              
    try:        
        ds['995_sigma_theta'] = ds35['pt']
    except Exception as e:
        pass              
    try:        
        ds['995_u_wind_component'] = ds35['u']
    except Exception as e:
        pass              
    try:        
        ds['995_v_wind_component'] = ds35['v']
    except Exception as e:
        pass              
    try:        
        ds['995_vertical_velocity'] = ds35['w']
    except Exception as e:
        pass              
    try:        
        ds['potential_vorticity'] = ds36['pv']
    except Exception as e:
        pass              
    try:        
        ds['theta_level_u_wind_component'] = ds37['u']
    except Exception as e:
        pass              
    try:        
        ds['theta_level_v_wind_component'] = ds38['v']
    except Exception as e:
        pass              
    try:        
        ds['theta_level_temperature'] = ds39['t']
    except Exception as e:
        pass              
    try:        
        ds['theta_level_montgomery_potential'] = ds40['mont']
    except Exception as e:
        pass              
    try:        
        ds['potential_vorticity_level_u_wind_component'] = ds41['u']
    except Exception as e:
        pass              
    try:        
        ds['potential_vorticity_level_v_wind_component'] = ds41['v']
    except Exception as e:
        pass              
    try:        
        ds['potential_vorticity_level_temperature'] = ds41['t']
    except Exception as e:
        pass                
    try:        
        ds['potential_vorticity_level_geopotential_height'] = ds41['gh']
    except Exception as e:
        pass        
    try:        
        ds['potential_vorticity_level_air_pressure'] = ds41['pres']
    except Exception as e:
        pass        
    try:        
        ds['potential_vorticity_level_vertical_speed_shear'] = ds41['vwsh']
    except Exception as e:
        pass        
    try:        
        ds['mixed_layer_air_temperature'] = ds42['t']
    except Exception as e:
        pass        
    try:        
        ds['mixed_layer_relative_humidity'] = ds42['r']
    except Exception as e:
        pass        
    try:        
        ds['mixed_layer_specific_humidity'] = ds42['q']
    except Exception as e:
        pass        
    try:        
        ds['mixed_layer_u_wind_component'] = ds42['u']
    except Exception as e:
        pass        
    try:        
        ds['mixed_layer_v_wind_component'] = ds42['v']
    except Exception as e:
        pass        
    try:        
        ds['mixed_layer_dew_point'] = ds43['dpt']
    except Exception as e:
        pass        
    try:        
        ds['mixed_layer_precipitable_water'] = ds44['pwat']
    except Exception as e:
        pass        
    try:        
        ds['parcel_lifted_index_to_500hPa'] = ds45['pli']
    except Exception as e:
        pass        
    try:        
        ds['mixed_layer_cape'] = ds46['cape']
    except Exception as e:
        pass        
    try:        
        ds['mixed_layer_cin'] = ds47['cin']
    except Exception as e:
        pass        
    try:        
        ds['pressure_level_from_which_a_parcel_was_lifted'] = ds48['plpl']
    except Exception as e:
        pass   

    try:
        ds = ds.drop_vars('unknown')
    except Exception as e:
        pass

    clear_gefs_idx_files(paths)

    return ds

