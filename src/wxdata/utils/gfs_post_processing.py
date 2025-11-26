"""
This file hosts the function responsible for GFS data post-processing. 

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
from wxdata.utils.coords import shift_longitude 

sys.tracebacklimit = 0
logging.disable()


def primary_gfs_post_processing(path):
    
    """
    This function post-processes the GFS0P25 and GFS0P50 GRIB Primary Variable Keys into Plain-Language Variable Keys
    
    Required Arguments:
    
    1) path (String) - The path to the files.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray.array of GFS0P25 data in Plain Language Keys.    
    
    Post-Process Variable Keys By Model
    -----------------------------------
    
    GFS0P25
    -------
    
    'mslp'
    'mslp_eta_reduction'
    'hybrid_level_cloud_mixing_ratio'
    'hybrid_level_ice_water_mixing_ratio'
    'hybrid_level_rain_mixing_ratio'
    'hybrid_level_snow_mixing_ratio'
    'hybrid_level_graupel'
    'hybrid_level_derived_radar_reflectivity'
    'boundary_layer_wind_u_component'
    'boundary_layer_wind_v_component'
    'ventilation_rate'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'specific_humidity'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'u_wind_component'
    'v_wind_component'
    'absolute_vorticity'
    'ozone_mixing_ratio'
    'total_cloud_cover'
    'ice_water_mixing_ratio'
    'rain_mixing_ratio'
    'cloud_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'derived_radar_reflectivity'
    '2m_temperature'
    '2m_specific_humidity'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'low_level_u_wind_component'
    'low_level_v_wind_component'
    'low_level_temperature'
    'low_level_specific_humidity'
    'pressure_height_above_ground'
    '100m_u_wind_component'
    '100m_v_wind_component'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    'liquid_volumetric_soil_moisture_non_frozen'
    'temperature_height_above_sea'
    'u_wind_component_height_above_sea'
    'v_wind_component_height_above_sea'
    'precipitable_water'
    'cloud_water'
    'entire_atmosphere_relative_humidity'
    'total_ozone'
    'low_cloud_cover'
    'middle_cloud_cover'
    'high_cloud_cover'
    'cloud_ceiling_height'
    'storm_relative_helicity'
    'u_component_of_storm_motion'
    'v_component_of_storm_motion'
    'tropopause_pressure'
    'tropopause_standard_atmosphere_reference_height'
    'tropopause_height'
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
    'mixed_layer_temperature'
    'mixed_layer_relative_humidity'
    'mixed_layer_specific_humidity'
    'mixed_layer_u_wind_component'
    'mixed_layer_v_wind_component'
    'mixed_layer_cape'
    'mixed_layer_cin'
    'pressure_level_from_which_a_parcel_was_lifted'
    'sigma_layer_relative_humidity'
    '995_sigma_temperature'
    '995_sigma_theta'
    '995_sigma_relative_humdity'
    '995_u_wind_component'
    '995_v_wind_component'
    '995_vertical_velocity'
    'potential_vorticity_level_u_wind_component'
    'potential_vorticity_level_v_wind_component'
    'potential_vorticity_level_temperature'
    'potential_vorticity_level_geopotential_height'
    'potential_vorticity_level_air_pressure'
    'potential_vorticity_level_vertical_speed_shear' 
    
    GFS0P50
    -------
    
    'mslp'
    'mslp_eta_reduction'
    'hybrid_level_cloud_mixing_ratio'
    'hybrid_level_ice_water_mixing_ratio'
    'hybrid_level_rain_mixing_ratio'
    'hybrid_level_snow_mixing_ratio'
    'hybrid_level_graupel'
    'hybrid_level_derived_radar_reflectivity'
    'boundary_layer_wind_u_component'
    'boundary_layer_wind_v_component'
    'ventilation_rate'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'u_wind_component'
    'v_wind_component'
    'absolute_vorticity'
    'total_cloud_cover'
    'ice_water_mixing_ratio'
    'rain_mixing_ratio'
    'cloud_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'derived_radar_reflectivity'
    '2m_temperature'
    '2m_specific_humidity'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'low_level_u_wind_component'
    'low_level_v_wind_component'
    'low_level_temperature'
    'low_level_specific_humidity'
    'pressure_height_above_ground'
    '100m_u_wind_component'
    '100m_v_wind_component'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    'liquid_volumetric_soil_moisture_non_frozen'
    'temperature_height_above_sea'
    'u_wind_component_height_above_sea'
    'v_wind_component_height_above_sea'
    'precipitable_water'
    'cloud_water'
    'entire_atmosphere_relative_humidity'
    'total_ozone'
    'low_cloud_cover'
    'middle_cloud_cover'
    'high_cloud_cover'
    'cloud_ceiling_height'
    'storm_relative_helicity'
    'u_component_of_storm_motion'
    'v_component_of_storm_motion'
    'tropopause_pressure'
    'tropopause_standard_atmosphere_reference_height'
    'tropopause_height'
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
    'mixed_layer_temperature'
    'mixed_layer_relative_humidity'
    'mixed_layer_specific_humidity'
    'mixed_layer_u_wind_component'
    'mixed_layer_v_wind_component'
    'mixed_layer_cape'
    'mixed_layer_cin'
    'pressure_level_from_which_a_parcel_was_lifted'
    'sigma_layer_relative_humidity'
    '995_sigma_temperature'
    '995_sigma_theta'
    '995_sigma_relative_humdity'
    '995_u_wind_component'
    '995_v_wind_component'
    '995_vertical_velocity'
    'potential_vorticity_level_u_wind_component'
    'potential_vorticity_level_v_wind_component'
    'potential_vorticity_level_temperature'
    'potential_vorticity_level_geopotential_height'
    'potential_vorticity_level_air_pressure'
    'potential_vorticity_level_vertical_speed_shear'
    """
    
    clear_idx_files_in_path(path)
    files = sorted_paths(path)

    print(files)
    #try:
    ds = xr.open_mfdataset(files, 
                        concat_dim='step', 
                        combine='nested', 
                        coords='minimal', 
                        engine='cfgrib', 
                        compat='override', 
                        decode_timedelta=False,
                        filter_by_keys={'typeOfLevel': 'meanSea'})
    
    ds = shift_longitude(ds)
    #except Exception as e:
        #pass
    
    try:
        ds1 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'hybrid'})
        
        ds1 = shift_longitude(ds1)
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
                            filter_by_keys={'typeOfLevel': 'hybrid', 'shortName':'refd'})
        
        ds2 = shift_longitude(ds2)
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
                            filter_by_keys={'typeOfLevel': 'atmosphere'})
        
        ds3 = shift_longitude(ds3)
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
                            filter_by_keys={'typeOfLevel': 'surface'})
        
        ds4 = shift_longitude(ds4)
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
                            filter_by_keys={'typeOfLevel': 'planetaryBoundaryLayer'})
        
        ds5 = shift_longitude(ds5)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
        
        ds6 = shift_longitude(ds6)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'tcc'})
        
        ds7 = shift_longitude(ds7)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'clwmr'})
        
        ds8 = shift_longitude(ds8)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'icmr'})
        
        ds9 = shift_longitude(ds9)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'rwmr'})
        
        ds10 = shift_longitude(ds10)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'snmr'})
        ds11 = shift_longitude(ds11)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'shortName':'grle'})
        
        ds12 = shift_longitude(ds12)
    except Exception as e:
        pass
    
    
    try:
        ds13 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround'})
        
        ds13 = shift_longitude(ds13)
    except Exception as e:
        pass
    
    try:
        ds14 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','paramId':167})
        
        ds14 = shift_longitude(ds14)
    except Exception as e:
        pass
    
    try:
        ds15 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','paramId':174096})
        
        ds15 = shift_longitude(ds15)
    except Exception as e:
        pass
    
    try:
        ds16 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','paramId':168})
        
        ds16 = shift_longitude(ds16)
    except Exception as e:
        pass
    
    try:
        ds17 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','paramId':260242})
        
        ds17 = shift_longitude(ds17)
    except Exception as e:
        pass
    
    try:
        ds18 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','paramId':165})
        
        ds18 = shift_longitude(ds18)
    except Exception as e:
        pass
    
    try:
        ds19 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','paramId':166})
        
        ds19 = shift_longitude(ds19)
    except Exception as e:
        pass
    
    try:
        ds20 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','paramId':131})
        
        ds20 = shift_longitude(ds20)
    except Exception as e:
        pass
    
    try:
        ds21 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','paramId':132})
        
        ds21 = shift_longitude(ds21)
    except Exception as e:
        pass
    
    try:
        ds22 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','paramId':130})
        
        ds22 = shift_longitude(ds22)
    except Exception as e:
        pass
    
    try:
        ds23 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','paramId':133})
        
        ds23 = shift_longitude(ds23)
    except Exception as e:
        pass
    
    try:
        ds24 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','paramId':54})
        
        ds24 = shift_longitude(ds24)
    except Exception as e:
        pass
    
    try:
        ds25 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','paramId':228246})
        
        ds25 = shift_longitude(ds25)
    except Exception as e:
        pass
    
    try:
        ds26 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','paramId':228247})
        
        ds26 = shift_longitude(ds26)
    except Exception as e:
        pass
    
    try:
        ds27 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'depthBelowLandLayer'})
        
        ds27 = shift_longitude(ds27)
    except Exception as e:
        pass
    
    try:
        ds28 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveSea','paramId':130})
        
        ds28 = shift_longitude(ds28)
    except Exception as e:
        pass
    
    try:
        ds29 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveSea','paramId':131})
        
        ds29 = shift_longitude(ds29)
    except Exception as e:
        pass
    
    try:
        ds30 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveSea','paramId':132})
        
        ds30 = shift_longitude(ds30)
    except Exception as e:
        pass
    
    try:
        ds31 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'atmosphereSingleLayer'})
        
        ds31 = shift_longitude(ds31)
    except Exception as e:
        pass
    
    try:
        ds32 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'lowCloudLayer'})
        
        ds32 = shift_longitude(ds32)
    except Exception as e:
        pass
    
    try:
        ds33 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'middleCloudLayer'})
        
        ds33 = shift_longitude(ds33)
    except Exception as e:
        pass
    
    try:
        ds34 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'highCloudLayer'})
        
        ds34 = shift_longitude(ds34)
    except Exception as e:
        pass
    
    try:
        ds35 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'cloudCeiling'})
        
        ds35 = shift_longitude(ds35)
    except Exception as e:
        pass
    
    try:
        ds36 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer'})
        
        ds36 = shift_longitude(ds36)
    except Exception as e:
        pass
    
    try:
        ds37 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer','paramId':260070})
        
        ds37 = shift_longitude(ds37)
    except Exception as e:
        pass
    
    try:
        ds38 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer','paramId':260071})
        
        ds38 = shift_longitude(ds38)
    except Exception as e:
        pass
    
    try:
        ds39 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'tropopause'})
        
        ds39 = shift_longitude(ds39)
    except Exception as e:
        pass
    
    try:
        ds40 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'maxWind'})
        
        ds40 = shift_longitude(ds40)
    except Exception as e:
        pass
    
    try:
        ds41 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'isothermZero'})
        
        ds41 = shift_longitude(ds41)
    except Exception as e:
        pass
    
    try:
        ds42 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'highestTroposphericFreezing'})
        
        ds42 = shift_longitude(ds42)
    except Exception as e:
        pass
    
    try:
        ds43 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'})
        
        ds43 = shift_longitude(ds43)
    except Exception as e:
        pass
    
    try:
        ds44 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer','paramId':59})
        
        ds44 = shift_longitude(ds44)
    except Exception as e:
        pass
    
    try:
        ds45 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer','paramId':228001})
        
        ds45 = shift_longitude(ds45)
    except Exception as e:
        pass
    
    try:
        ds46 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer','paramId':260325})
        
        ds46 = shift_longitude(ds46)
    except Exception as e:
        pass
    
    try:
        ds47 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'sigmaLayer'})
        
        ds47 = shift_longitude(ds47)
    except Exception as e:
        pass
    
    try:
        ds48 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'sigma'})
        
        ds48 = shift_longitude(ds48)
    except Exception as e:
        pass
    
    try:
        ds49 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'potentialVorticity'})
        
        ds49 = shift_longitude(ds49)
    except Exception as e:
        pass
    
    try:     
        ds['mslp'] = ds['prmsl']
        ds = ds.drop_vars('prmsl')
    except Exception as e:
        pass  
    
    try:        
        ds['mslp_eta_reduction'] = ds['mslet']  
        ds = ds.drop_vars('mslet')
    except Exception as e:
        pass   
    
    try:        
        ds['hybrid_level_cloud_mixing_ratio'] = ds1['clwmr']
    except Exception as e:
        pass      
    
    try:
        ds['hybrid_level_ice_water_mixing_ratio'] = ds1['icmr']  
    except Exception as e:
        pass
    
    try:
        ds['hybrid_level_rain_mixing_ratio'] = ds1['rwmr']
    except Exception as e:
        pass
    
    try:
        ds['hybrid_level_snow_mixing_ratio'] = ds1['snmr']
    except Exception as e:
        pass
    
    try:
        ds['hybrid_level_graupel'] = ds1['grle']
    except Exception as e:
        pass
    
    try:
        ds['hybrid_level_derived_radar_reflectivity'] = ds2['refd']
    except Exception as e:
        pass
        
    try:
        ds['maximum_composite_reflectivity'] = ds3['refc']
    except Exception as e:
        pass
        
    try:
        ds['entire_atmosphere_total_cloud_cover'] = ds3['tcc']
    except Exception as e:
        pass
        
    try:
        ds['surface_visibility'] = ds4['vis']
    except Exception as e:
        pass
        
    try:
        ds['surface_wind_gust'] = ds4['gust']
    except Exception as e:
        pass
        
    try:
        ds['haines_index'] = ds4['hindex']
    except Exception as e:
        pass
        
    try:
        ds['surface_pressure'] = ds['sp']
    except Exception as e:
        pass
        
    try:
        ds['orography'] = ds4['orog']
    except Exception as e:
        pass
        
    try:
        ds['surface_temperature'] = ds4['t']
    except Exception as e:
        pass
    
    try:
        ds['plant_canopy_surface_water'] = ds4['cnwat']
    except Exception as e:
        pass
    
    try:
        ds['water_equivalent_of_accumulated_snow_depth'] = ds4['sdwe']
    except Exception as e:
        pass
    
    try:     
        ds['snow_depth'] = ds4['sde']
    except Exception as e:
        pass  
    
    try:     
        ds['sea_ice_thickness'] = ds4['sithick']
    except Exception as e:
        pass   
    
    try:        
        ds['percent_frozen_precipitation'] = ds4['cpofp']
    except Exception as e:
        pass  
    
    try:        
        ds['precipitation_rate'] = ds4['prate']
    except Exception as e:
        pass     
    
    try: 
        ds['categorical_snow'] = ds4['csnow']
    except Exception as e:
        pass  
    
    try:
        ds['categorical_ice_pellets'] = ds4['cicep']
    except Exception as e:
        pass
    
    try: 
        ds['categorical_freezing_rain'] = ds4['cfrzr']
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_rain'] = ds4['crain']
    except Exception as e:
        pass  
    
    try:        
        ds['surface_roughness'] = ds4['fsr']
    except Exception as e:
        pass        
    
    try:        
        ds['frictional_velocity'] = ds4['fricv']
    except Exception as e:
        pass      
        
    try:
        ds['vegetation'] = ds4['veg']
    except Exception as e:
        pass
    
    try:
        ds['soil_type'] = ds4['slt']
    except Exception as e:
        pass
    
    try:        
        ds['wilting_point'] = ds4['wilt']
    except Exception as e:
        pass        
    
    try:        
        ds['field_capacity'] = ds4['fldcp']
    except Exception as e:
        pass       
     
    try:        
        ds['sunshine_duration'] = ds4['SUNSD']
    except Exception as e:
        pass     
       
    try:        
        ds['surface_lifted_index'] = ds4['lftx']
    except Exception as e:
        pass   
         
    try:        
        ds['best_4_layer_lifted_index'] = ds4['lftx4']
    except Exception as e:
        pass    
    
    try:        
        ds['surface_cape'] = ds4['cape']
    except Exception as e:
        pass    
        
    try:        
        ds['surface_cin'] = ds4['cin']
    except Exception as e:
        pass 
    
    try:        
        ds['sea_ice_area_fraction'] = ds4['siconc']
    except Exception as e:
        pass        
    
    try:
        ds['sea_ice_temperature'] = ds4['sit']
    except Exception as e:
        pass
    
    try:
        ds['boundary_layer_wind_u_component'] = ds5['u']
    except Exception as e:
        pass
    
    try:
        ds['boundary_layer_wind_v_component'] = ds5['v']
    except Exception as e:
        pass
    
    try:
        ds['ventilation_rate'] = ds5['VRATE']
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height'] = ds6['gh']
    except Exception as e:
        pass
    
    try:
        ds['air_temperature'] = ds6['t']
    except Exception as e:
        pass
    
    try:
        ds['relative_humidity'] = ds6['r']
    except Exception as e:
        pass
    
    try:
        ds['specific_humidity'] = ds6['q']
    except Exception as e:
        pass
    
    try:
        ds['vertical_velocity'] = ds6['w']
    except Exception as e:
        pass
    
    try:
        ds['geometric_vertical_velocity'] = ds6['wz']
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component'] = ds6['u']
    except Exception as e:
        pass

    try:
        ds['v_wind_component'] = ds6['v']
    except Exception as e:
        pass
    
    try:
        ds['absolute_vorticity'] = ds6['absv']
    except Exception as e:
        pass
    
    try:
        ds['ozone_mixing_ratio'] = ds6['o3mr']
    except Exception as e:
        pass
    
    try:
        ds['total_cloud_cover'] = ds7['tcc']
    except Exception as e:
        pass
    
    try:
        ds['ice_water_mixing_ratio'] = ds8['clwmr']  
    except Exception as e:
        pass
    
    try:
        ds['rain_mixing_ratio'] = ds9['icmr']
    except Exception as e:
        pass
    
    try:        
        ds['cloud_mixing_ratio'] = ds10['rwmr']
    except Exception as e:
        pass      
    
    try:
        ds['snow_mixing_ratio'] = ds11['snmr']
    except Exception as e:
        pass
    
    try:
        ds['graupel'] = ds12['grle']
    except Exception as e:
        pass
    
    try:
        ds['derived_radar_reflectivity'] = ds13['refd']
    except Exception as e:
        pass
    
    try:
        ds['2m_temperature'] = ds14['t2m']
    except Exception as e:
        pass
    
    try:
        ds['2m_specific_humidity'] = ds15['sh2']
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point'] = ds16['d2m']
    except Exception as e:
        pass
    
    try:
        ds['2m_relative_humidity'] = ds17['r2']
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point_depression'] = ds['2m_temperature'] - ds['2m_dew_point']
    except Exception as e:
        pass
    
    try:
        ds['10m_u_wind_component'] = ds18['u10']
    except Exception as e:
        pass
    
    try:
        ds['10m_v_wind_component'] = ds19['v10']
    except Exception as e:
        pass
    
    try:
        ds['low_level_u_wind_component'] = ds20['u']
    except Exception as e:
        pass
    
    try:
        ds['low_level_v_wind_component'] = ds21['v']
    except Exception as e:
        pass
    
    try:
        ds['low_level_temperature'] = ds22['t']
    except Exception as e:
        pass
    
    try:
        ds['low_level_specific_humidity'] = ds23['q']
    except Exception as e:
        pass
    
    try:
        ds['pressure_height_above_ground'] = ds24['pres']
    except Exception as e:
        pass
    
    try:
        ds['100m_u_wind_component'] = ds25['u100']
    except Exception as e:
        pass
    
    try:
        ds['100m_v_wind_component'] = ds26['v100']
    except Exception as e:
        pass
    
    try:
        ds['soil_temperature'] = ds27['st']
    except Exception as e:
        pass
    
    try:        
        ds['volumetric_soil_moisture_content'] = ds27['soilw']
    except Exception as e:
        pass
    
    try:        
        ds['liquid_volumetric_soil_moisture_non_frozen'] = ds27['soill']
    except Exception as e:
        pass    
    
    try:
        ds['temperature_height_above_sea'] = ds28['t']
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component_height_above_sea'] = ds29['u']
    except Exception as e:
        pass
    
    try:
        ds['v_wind_component_height_above_sea'] = ds30['v']
    except Exception as e:
        pass
    
    try:
        ds['precipitable_water'] = ds31['pwat']
    except Exception as e:
        pass
    
    try:
        ds['cloud_water'] = ds31['cwat']
    except Exception as e:
        pass
    
    try:
        ds['entire_atmosphere_relative_humidity'] = ds31['r']
    except Exception as e:
        pass
    
    try:
        ds['total_ozone'] = ds31['tozne']
    except Exception as e:
        pass
    
    try:
        ds['low_cloud_cover'] = ds32['lcc']
    except Exception as e:
        pass
    
    try:
        ds['middle_cloud_cover'] = ds33['mcc']
    except Exception as e:
        pass
        
    try:
        ds['high_cloud_cover'] = ds34['hcc']
    except Exception as e:
        pass
    
    try:
        ds['cloud_ceiling_height'] = ds35['gh']
    except Exception as e:
        pass
    
    try:
        ds['storm_relative_helicity'] = ds36['hlcy']
    except Exception as e:
        pass
    
    try:        
        ds['u_component_of_storm_motion'] = ds37['ustm']
    except Exception as e:
        pass     
       
    try:        
        ds['v_component_of_storm_motion'] = ds38['vstm']
    except Exception as e:
        pass      
    
    try:
        ds['tropopause_pressure'] = ds39['trpp']
    except Exception as e:
        pass
    
    try:
        ds['tropopause_standard_atmosphere_reference_height'] = ds39['icaht']
    except Exception as e:
        pass
    
    try:
        ds['tropopause_height'] = ds39['gh']
    except Exception as e:
        pass
    
    try:        
        ds['tropopause_u_wind_component'] = ds39['u']
    except Exception as e:
        pass        
    
    try:        
        ds['tropopause_v_wind_component'] = ds39['v']
    except Exception as e:
        pass      
            
    try:        
        ds['tropopause_temperature'] = ds39['t']
    except Exception as e:
        pass    
              
    try:        
        ds['tropopause_vertical_speed_shear'] = ds39['vwsh']
    except Exception as e:
        pass  
                
    try:        
        ds['max_wind_u_component'] = ds40['u']
    except Exception as e:
        pass  
                
    try:        
        ds['max_wind_v_component'] = ds40['v']
    except Exception as e:
        pass   
    
    try:        
        ds['zero_deg_c_isotherm_geopotential_height'] = ds41['gh']
    except Exception as e:
        pass       
           
    try:        
        ds['zero_deg_c_isotherm_relative_humidity'] = ds41['r']
    except Exception as e:
        pass  
    
    try:        
        ds['highest_tropospheric_freezing_level_geopotential_height'] = ds42['gh']
    except Exception as e:
        pass   
               
    try:        
        ds['highest_tropospheric_freezing_level_relative_humidity'] = ds42['r']
    except Exception as e:
        pass  
    
    try:
        ds['mixed_layer_temperature'] = ds43['t']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_relative_humidity'] = ds43['r']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_specific_humidity'] = ds43['q']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_u_wind_component'] = ds43['u']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_v_wind_component'] = ds43['v']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_cape'] = ds44['cape']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_cin'] = ds45['cin']
    except Exception as e:
        pass
    
    try:
        ds['pressure_level_from_which_a_parcel_was_lifted'] = ds46['plpl']
    except Exception as e:
        pass
    
    try:
        ds['sigma_layer_relative_humidity'] = ds47['r']
    except Exception as e:
        pass
    
    try:        
        ds['995_sigma_temperature'] = ds48['t']
    except Exception as e:
        pass  
                
    try:        
        ds['995_sigma_theta'] = ds48['pt']
    except Exception as e:
        pass   
    
    try:        
        ds['995_sigma_relative_humdity'] = ds48['r']
    except Exception as e:
        pass       
    
    try:        
        ds['995_u_wind_component'] = ds48['u']
    except Exception as e:
        pass     
             
    try:        
        ds['995_v_wind_component'] = ds48['v']
    except Exception as e:
        pass    
              
    try:        
        ds['995_vertical_velocity'] = ds48['w']
    except Exception as e:
        pass 
    
    try:        
        ds['potential_vorticity_level_u_wind_component'] = ds49['u']
    except Exception as e:
        pass       
           
    try:        
        ds['potential_vorticity_level_v_wind_component'] = ds49['v']
    except Exception as e:
        pass            
      
    try:        
        ds['potential_vorticity_level_temperature'] = ds49['t']
    except Exception as e:
        pass        
            
    try:        
        ds['potential_vorticity_level_geopotential_height'] = ds49['gh']
    except Exception as e:
        pass      
      
    try:        
        ds['potential_vorticity_level_air_pressure'] = ds49['pres']
    except Exception as e:
        pass       
     
    try:        
        ds['potential_vorticity_level_vertical_speed_shear'] = ds49['vwsh']
    except Exception as e:
        pass    
    
    clear_idx_files_in_path(path)
    
    return ds


def secondary_gfs_post_processing(path):
    
    """
    This function post-processes the GFS0P25 and GFS0P50 GRIB Primary Variable Keys into Plain-Language Variable Keys
    
    Required Arguments:
    
    1) path (String) - The path to the files.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray.array of GFS0P25 data in Plain Language Keys.   
    
    Post-processed variable keys
    ----------------------------
    
    'u_wind_component'
    'v_wind_component'
    'air_temperature'
    'relative_humidity'
    'absolute_vorticity'
    'geopotential_height'
    'ozone_mixing_ratio'
    'total_cloud_cover'
    'cloud_mixing_ratio'
    'ice_water_mixing_ratio'
    'rain_water_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'liquid_volumetric_soil_moisture_non_frozen'
    'plant_canopy_surface_water'
    'sea_ice_thickness'
    'temperature_height_above_sea'
    'u_wind_component_height_above_sea'
    'v_wind_component_height_above_sea'
    'mixed_layer_temperature'
    'mixed_layer_relative_humidity'
    'mixed_layer_specific_humidity'
    'mixed_layer_u_wind_component'
    'mixed_layer_v_wind_component'
    'potential_vorticity_level_u_wind_component'
    'potential_vorticity_level_v_wind_component'
    'potential_vorticity_level_temperature'
    'potential_vorticity_level_geopotential_height'
    'potential_vorticity_level_air_pressure'
    'potential_vorticity_level_vertical_speed_shear' 
    
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
        
        ds = shift_longitude(ds)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260131})
        
        ds1 = shift_longitude(ds1)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':228164})
        
        ds2 = shift_longitude(ds2)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260018})
        
        ds3 = shift_longitude(ds3)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260019})
        
        ds4 = shift_longitude(ds4)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260020})
        
        ds5 = shift_longitude(ds5)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260021})
        
        ds6 = shift_longitude(ds6)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260028})
        
        ds7 = shift_longitude(ds7)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':135})
        
        ds8 = shift_longitude(ds8)
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260238})
        
        ds9 = shift_longitude(ds9)
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
                            filter_by_keys={'typeOfLevel': 'depthBelowLandLayer'})
        
        ds10 = shift_longitude(ds10)
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
                            filter_by_keys={'typeOfLevel': 'surface'})
        
        ds11 = shift_longitude(ds11)
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
                            filter_by_keys={'typeOfLevel': 'heightAboveSea'})
        
        ds12 = shift_longitude(ds12)
    except Exception as e:
        pass
    
    try:
        ds13 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'})
        
        ds13 = shift_longitude(ds13)
    except Exception as e:
        pass 
    
    try:
        ds14 = xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'potentialVorticity'})
        
        ds14 = shift_longitude(ds14)
    except Exception as e:
        pass 
    
    try:
        ds['u_wind_component'] = ds['u']
        ds = ds.drop_vars('u')
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
        ds['relative_humidity'] = ds['r']
        ds = ds.drop_vars('r')
    except Exception as e:
        pass
    
    try:
        ds['absolute_vorticity'] = ds['absv']
        ds = ds.drop_vars('absv')
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height'] = ds['gh']
        ds = ds.drop_vars('gh')
    except Exception as e:
        pass
    
    try:
        ds['vertical_speed_shear'] = ds['wvsh']
        ds = ds.drop_vars('wvsh')
    except Exception as e:
        pass
    
    try:
        ds['ozone_mixing_ratio'] = ds1['o3mr']
    except Exception as e:
        pass
    
    try:
        ds['total_cloud_cover'] = ds2['tcc']
    except Exception as e:
        pass
    
    try:
        ds['cloud_mixing_ratio'] = ds3['clwmr']
    except Exception as e:
        pass
    
    try:
        ds['ice_water_mixing_ratio'] = ds4['icmr']
    except Exception as e:
        pass
    
    try:
        ds['rain_water_mixing_ratio'] = ds5['rwmr']
    except Exception as e:
        pass
    
    try:
        ds['snow_mixing_ratio'] = ds6['snmr']
    except Exception as e:
        pass
    
    try:
        ds['graupel'] = ds7['grle']
    except Exception as e:
        pass
    
    try:
        ds['vertical_velocity'] = ds8['w']
    except Exception as e:
        pass
    
    try:
        ds['geometric_vertical_velocity'] = ds9['wz']
    except Exception as e:
        pass
    
    try:
        ds['liquid_volumetric_soil_moisture_non_frozen'] = ds10['soill']
    except Exception as e:
        pass
    
    try:
        ds['plant_canopy_surface_water'] = ds11['cnwat']
    except Exception as e:
        pass
    
    try:
        ds['sea_ice_thickness'] = ds11['sithick']
    except Exception as e:
        pass
    
    try:
        ds['temperature_height_above_sea'] = ds12['t']
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component_height_above_sea'] = ds12['u']
    except Exception as e:
        pass
    
    try:
        ds['v_wind_component_height_above_sea'] = ds12['v']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_temperature'] = ds13['t']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_relative_humidity'] = ds13['r']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_specific_humidity'] = ds13['q']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_u_wind_component'] = ds13['u']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_v_wind_component'] = ds13['v']
    except Exception as e:
        pass
    
    try:        
        ds['potential_vorticity_level_u_wind_component'] = ds14['u']
    except Exception as e:
        pass       
           
    try:        
        ds['potential_vorticity_level_v_wind_component'] = ds14['v']
    except Exception as e:
        pass            
      
    try:        
        ds['potential_vorticity_level_temperature'] = ds14['t']
    except Exception as e:
        pass        
            
    try:        
        ds['potential_vorticity_level_geopotential_height'] = ds14['gh']
    except Exception as e:
        pass      
      
    try:        
        ds['potential_vorticity_level_air_pressure'] = ds14['pres']
    except Exception as e:
        pass       
     
    try:        
        ds['potential_vorticity_level_vertical_speed_shear'] = ds14['vwsh']
    except Exception as e:
        pass    
    
    clear_idx_files_in_path(path)
    
    return ds