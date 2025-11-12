"""
This file hosts functions that download various types of GEFS Data

(C) Eric J. Drewitz 2025
"""

import wxdata.client.client as client
import os
import warnings
import wxdata.utils.gefs_post_processing as gefs_post_processing
warnings.filterwarnings('ignore')

from wxdata.gefs.file_funcs import(
    
    build_directory,
    clear_idx_files,
    clear_empty_files
    
)
from wxdata.gefs.url_scanners import(
    
    gefs_0p50_url_scanner,
    gefs_0p50_secondary_parameters_url_scanner,
    gefs_0p25_url_scanner
)

from wxdata.gefs.process import(
    
    process_gefs_data,
    process_gefs_secondary_parameters_data
    
)

from wxdata.utils.file_funcs import(
     custom_branch,
     custom_branches,
     clear_gefs_idx_files
)

from wxdata.calc.derived_fields import gefs_primary_derived_fields
from wxdata.calc.unit_conversion import convert_temperature_units
from wxdata.utils.file_scanner import local_file_scanner
from wxdata.utils.recycle_bin import *

def gefs0p50(cat='mean', 
             final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=True,
             variables=['total precipitation',
                        'convective available potential energy',
                        'categorical freezing rain',
                        'categorical ice pellets',
                        'categorical rain',
                        'categorical snow',
                        'convective inhibition',
                        'downward longwave radiation flux',
                        'downward shortwave radiation flux',
                        'geopotential height',
                        'ice thickness',
                        'latent heat net flux',
                        'pressure',
                        'mean sea level pressure',
                        'precipitable water',
                        'relative humidity',
                        'sensible heat net flux',
                        'snow depth',
                        'volumetric soil moisture content',
                        'total cloud cover',
                        'maximum temperature',
                        'minimum temperature',
                        'temperature',
                        'soil temperature',
                        'u-component of wind',
                        'upward longwave radiation flux',
                        'upward shortwave radiation flux',
                        'v-component of wind',
                        'vertical velocity',
                        'water equivalent of accumulated snow depth'],
            convert_temperature=True,
            convert_to='celsius',
            custom_directory=None,
            chunk_size=8192,
            notifications='off'):
    
    """
    This function downloads the latest GEFS0P50 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    12) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50
        -------------------------------
        
			'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'categorical rain'
            'categorical snow'
            'convective inhibition'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'geopotential height'
            'ice thickness'
            'latent heat net flux'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'sensible heat net flux'
            'snow depth'
            'volumetric soil moisture content'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'soil temperature'
            'u-component of wind'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'v-component of wind'
            'vertical velocity'
            'water equivalent of accumulated snow depth'
    
    
    Returns
    -------
    
    An xarray data array of the GEFS0P50 data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P50 files are saved to f:GEFS0P50/{cat} or in the case of ensemble members f:GEFS0P50/{cat}/{member}
    
    Variables
    ---------
    
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
    'wind_speed'
    'absolute_vortcity'
    'curvature_vorticity'
    'divergence'
    'dew_point'
    'temperature_advection'
    'vorticity_advection'
    'precipitable_water_advection'
    'humidity_advection'
    'potential_temperature'
    'mixing_ratio'
    'dry_lapse_rate'
    
    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass    
    
    
    cat = cat.lower()
    if custom_directory == None:
        
        paths = build_directory('gefs0p50', 
                                cat, 
                                members)

        clear_idx_files('gefs0p50', 
                        cat, 
                        members)
    
    else:
        if cat == 'members':
            paths = custom_branches(custom_directory)
            
        else:
            paths = custom_branch(custom_directory)
        
        clear_gefs_idx_files(paths)
    
    urls, filenames, run = gefs_0p50_url_scanner(cat, 
                                            final_forecast_hour,
                                            western_bound, 
                                            eastern_bound, 
                                            northern_bound, 
                                            southern_bound, 
                                            proxies, 
                                            step, 
                                            members,
                                            variables)
    
    try:
        download = local_file_scanner(paths[-1], 
                                        filenames[-1],
                                        'nomads',
                                        run)
    except Exception as e:
        download = local_file_scanner(paths, 
                                        filenames,
                                        'nomads',
                                        run)       
    
    if download == True:
        print(f"Data downloading...")
        
        try:
            for path in paths:
                for file in os.listdir(f"{path}"):
                    os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        if cat != 'members':
            for path in paths:
                for url, filename in zip(urls, filenames):
                    client.get_gridded_data(f"{url}",
                                path,
                                f"{filename}.grib2",
                                proxies=proxies,
                                chunk_size=chunk_size,
                                notifications=notifications)                                                                 
                            
        else:
            start = 0
            increment = int(len(filenames)/len(members))
            stop = increment
            for path in paths:
                for u, f in zip(range(start, stop, 1), range(start, stop, 1)):
                    client.get_gridded_data(f"{urls[u]}",
                                path,
                                f"{filenames[f]}.grib2",
                                proxies=proxies,
                                chunk_size=chunk_size,
                                notifications=notifications)  
                                
                start = start + increment
                stop = stop + increment     
                        
        print(f"Download Complete.")        
    else:
        print(f"User has the current dataset.\nSkipping download.")
        
    if process_data == True:
        print(f"Data Processing...")
        clear_empty_files(paths)
        
        if custom_directory == None:
            print(f"")
            ds = process_gefs_data('gefs0p50', 
                                        cat,
                                        members)
                    
            clear_idx_files('gefs0p50', 
                        cat, 
                        members)
            
        else:
            ds = gefs_post_processing.primary_gefs_post_processing(paths)
            
            gefs_post_processing.clear_gefs_idx_files(paths)
            
        if convert_temperature == True:
            ds = convert_temperature_units(ds, 
                                            convert_to,
                                            cat=cat)
                
        else:
            pass
        
        ds = gefs_primary_derived_fields(ds,
                                 convert_temperature,
                                 convert_to)
            
        print(f"Data Processing Complete.")
        return ds
    else:
        pass

def gefs0p50_secondary_parameters(cat='mean', 
             final_forecast_hour=384, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=True,
             variables=['best lifted index',
                        '5 wave geopotential height',
                        'absolute vorticity',
                        'temperature',
                        'dew point',
                        'convective precipitation',
                        'albedo',
                        'apparent temperature',
                        'brightness temperature',
                        'convective available potential energy',
                        'clear sky uv-b downward solar flux',
                        'convective inhibition',
                        'cloud mixing ratio',
                        'plant canopy surface water',
                        'percent frozen precipitaion',
                        'convective precipitation rate',
                        'cloud water',
                        'cloud work function',
                        'uv-b downward solar flux',
                        'field capacity',
                        'surface friction velocity',
                        'ground heat flux',
                        'wind gust',
                        'geopotential height',
                        'haines index',
                        'storm relative helicity',
                        'planetary boundary layer height',
                        'icao standard atmosphere reference height',
                        'ice cover',
                        'icing',
                        'icing severity',
                        'land cover',
                        'surface lifted index',
                        'montgomery stream function',
                        'mslp (eta model reduction)',
                        'large scale non-convective precipitation',
                        'ozone mixing ratio',
                        'potential evaporation rate',
                        'parcel lifted index (to 500mb)',
                        'pressure level from which parcel was lifted',
                        'potential temperature',
                        'precipitation rate',
                        'pressure',
                        'potential vorticity',
                        'precipitable water',
                        'relative humidity',
                        'surface roughness',
                        'snow phase-change heat flux',
                        'snow cover',
                        'liquid volumetric soil moisture (non-frozen)',
                        'volumetric soil moisture content',
                        'specific humidity',
                        'sunshine duration',
                        'total cloud cover',
                        'total ozone',
                        'soil temperature',
                        'momentum flux (u-component)',
                        'u-component of wind',
                        'zonal flux of gravity wave stress',
                        'u-component of storm motion',
                        'upward shortwave radiation flux',
                        'momentum flux (v-component)',
                        'v-component of wind',
                        'meridional flux of gravity wave stress',
                        'visibility',
                        'ventilation rate',
                        'v-component of storm motion',
                        'vertical velocity',
                        'vertical speed shear',
                        'water runoff',
                        'wilting point'],
             convert_temperature=True,
             convert_to='celsius',
            custom_directory=None,
            chunk_size=8192,
            notifications='off'):
                        
    
    """
    This function downloads the latest GEFS0P50 SECONDARY PARAMETERS data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='control'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50 SECONDARY PARAMETERS
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    12) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50 SECONDARY PARAMETERS
        ----------------------------------------------------
        
        'best lifted index'
        '5 wave geopotential height'
        'absolute vorticity'
        'temperature'
        'dew point'
        'convective precipitation'
        'albedo'
        'apparent temperature'
        'brightness temperature'
        'convective available potential energy'
        'clear sky uv-b downward solar flux'
        'convective inhibition'
        'cloud mixing ratio'
        'plant canopy surface water'
        'percent frozen precipitaion'
        'convective precipitation rate'
        'cloud water'
        'cloud work function'
        'uv-b downward solar flux'
        'field capacity'
        'surface friction velocity'
        'ground heat flux'
        'wind gust'
        'geopotential height'
        'haines index'
        'storm relative helicity'
        'planetary boundary layer height'
        'icao standard atmosphere reference height'
        'ice cover'
        'icing'
        'icing severity'
        'land cover'
        'surface lifted index'
        'montgomery stream function'
        'mslp (eta model reduction)'
        'large scale non-convective precipitation'
        'ozone mixing ratio'
        'potential evaporation rate'
        'parcel lifted index (to 500mb)'
        'pressure level from which parcel was lifted'
        'potential temperature'
        'precipitation rate'
        'pressure'
        'potential vorticity'
        'precipitable water'
        'relative humidity'
        'surface roughness'
        'snow phase-change heat flux'
        'snow cover'
        'liquid volumetric soil moisture (non-frozen)'
        'volumetric soil moisture content'
        'specific humidity'
        'sunshine duration'
        'total cloud cover'
        'total ozone'
        'soil temperature'
        'momentum flux (u-component)'
        'u-component of wind'
        'zonal flux of gravity wave stress'
        'u-component of storm motion'
        'upward shortwave radiation flux'
        'momentum flux (v-component)'
        'v-component of wind'
        'meridional flux of gravity wave stress'
        'visibility'
        'ventilation rate'
        'v-component of storm motion'
        'vertical velocity'
        'vertical speed shear'
        'water runoff'
        'wilting point'
    
    
    Returns
    -------
    
    An xarray data array of the GEFS0P50 SECONDARY PARAMETERS data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P50 SECONDARY PARAMETERS files are saved to f:GEFS0P50 SECONDARY PARAMETERS/{cat} or in the case of ensemble members f:GEFS0P50 SECONDARY PARAMETERS/{cat}/{member}
    
    Variables
    ---------
    
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
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    cat = cat.lower()
    
    if custom_directory == None:
        paths = build_directory('gefs0p50 secondary parameters', 
                                cat, 
                                members)

        clear_idx_files('gefs0p50 secondary parameters', 
                        cat, 
                        members)
        
    else:
        if cat == 'members':
            paths = custom_branches(custom_directory)
            
        else:
            paths = custom_branch(custom_directory)
        
        clear_gefs_idx_files(paths)
    
    urls, filenames, run = gefs_0p50_secondary_parameters_url_scanner(cat, 
                                            final_forecast_hour,
                                            western_bound, 
                                            eastern_bound, 
                                            northern_bound, 
                                            southern_bound, 
                                            proxies, 
                                            step, 
                                            members, 
                                            variables)
    
    try:
        download = local_file_scanner(paths[-1], 
                                        filenames[-1],
                                        'nomads',
                                        run)
    except Exception as e:
        download = local_file_scanner(paths, 
                                        filenames,
                                        'nomads',
                                        run)       
    
    if download == True:
        print(f"Data downloading...")

        try:
            for path in paths:
                for file in os.listdir(f"{path}"):
                    os.remove(f"{path}/{file}")
        except Exception as e:
            pass        
                    
        if cat != 'members' and cat != 'mean' and cat != 'spread':
            for path in paths:
                for url, filename in zip(urls, filenames):
                    client.get_gridded_data(f"{url}",
                                path,
                                f"{filename}.grib2",
                                proxies=proxies,
                                chunk_size=chunk_size,
                                notifications=notifications)       
        else:
            start = 0
            increment = int(len(filenames)/len(members))
            stop = increment
            for path in paths:
                for u, f in zip(range(start, stop, 1), range(start, stop, 1)):
                    client.get_gridded_data(f"{urls[u]}",
                                path,
                                f"{filenames[f]}.grib2",
                                proxies=proxies,
                                chunk_size=chunk_size,
                                notifications=notifications)    
                                
                start = start + increment
                stop = stop + increment            
        print(f"Download Complete.")        
    else:
        print(f"User has the current dataset.\nSkipping download.")
    
    if process_data == True:
        print(f"Data Processing...")
        
        ds = process_gefs_secondary_parameters_data('gefs0p50 secondary parameters', 
                                    cat,
                                    members)
        
        if convert_temperature == True:
            ds = convert_temperature_units(ds, 
                                           convert_to, 
                                           cat=cat)
                
        clear_idx_files('gefs0p50 secondary parameters', 
                    cat, 
                    members)
        
        print(f"Data Processing Complete.")
        return ds
    else:
        pass
    
def gefs0p25(cat='mean', 
             final_forecast_hour=240, 
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90, 
             proxies=None, 
             step=3, 
             members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             process_data=True,
             clear_recycle_bin=True,
             variables=['total precipitation',
                        'convective available potential energy',
                        'categorical freezing rain',
                        'categorical ice pellets',
                        'convective inhibition',
                        'percent frozen precipitaion',
                        'categorical rain',
                        'categorical snow',
                        'downward longwave radiation flux',
                        'downward shortwave radiation flux',
                        'dew point',
                        'wind gust',
                        'geopotential height',
                        'storm relative helicity',
                        'ice thickness',
                        'latent heat net flux',
                        'pressure',
                        'mean sea level pressure',
                        'precipitable water',
                        'relative humidity',
                        'sensible heat net flux',
                        'snow depth',
                        'volumetric soil moisture content',
                        'total cloud cover',
                        'maximum temperature',
                        'minimum temperature',
                        'temperature',
                        'soil temperature',
                        'u-component of wind',
                        'upward longwave radiation flux',
                        'upward shortwave radiation flux',
                        'v-component of wind',
                        'visibility',
                        'water equivalent of accumulated snow depth'],
             convert_temperature=True,
             convert_to='celsius',
             custom_directory=None,
             chunk_size=8192,
             notifications='off'):
    
    """
    This function downloads the latest GEFS0P25 data for a region specified by the user
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (string) - Default='mean'. The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - Default = 240. The final forecast hour the user wishes to download. The GEFS0P25
    goes out to 240 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    240 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
    
    8) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 
    
    9) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    12) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P25
        -------------------------------
        
        'total precipitation'
        'convective available potential energy'
        'categorical freezing rain'
        'categorical ice pellets'
        'convective inhibition'
        'percent frozen precipitaion'
        'categorical rain'
        'categorical snow'
        'downward longwave radiation flux'
        'downward shortwave radiation flux'
        'dew point'
        'wind gust'
        'geopotential height'
        'storm relative helicity'
        'ice thickness'
        'latent heat net flux'
        'pressure'
        'mean sea level pressure'
        'precipitable water'
        'relative humidity'
        'sensible heat net flux'
        'snow depth'
        'volumetric soil moisture content'
        'total cloud cover'
        'maximum temperature'
        'minimum temperature'
        'temperature'
        'soil temperature'
        'u-component of wind'
        'upward longwave radiation flux'
        'upward shortwave radiation flux'
        'v-component of wind'
        'visibility'
        'water equivalent of accumulated snow depth'
    
    
    Returns
    -------
    
    An xarray data array of the GEFS0P25 data specified to the coordinate boundaries and variable list the user specifies. 
    
    GEFS0P25 files are saved to f:GEFS0P25/{cat} or in the case of ensemble members f:GEFS0P25/{cat}/{member}
    
    Variables
    ---------
    
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
    '2m_dew_point_depression'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'mixed_layer_cape'
    'mixed_layer_cin'
    '3km_helicity'
    
    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass    
    
    cat = cat.lower()
    
    if custom_directory == None:
        paths = build_directory('gefs0p25', 
                                cat, 
                                members)

        clear_idx_files('gefs0p25', 
                        cat, 
                        members)
        
    else:
        if cat == 'members':
            paths = custom_branches(custom_directory)
            
        else:
            paths = custom_branch(custom_directory)
        
        clear_gefs_idx_files(paths)
    
    urls, filenames, run = gefs_0p25_url_scanner(cat, 
                                            final_forecast_hour,
                                            western_bound, 
                                            eastern_bound, 
                                            northern_bound, 
                                            southern_bound, 
                                            proxies, 
                                            step, 
                                            members,
                                            variables)
    
    try:
        download = local_file_scanner(paths[-1], 
                                        filenames[-1],
                                        'nomads',
                                        run)
    except Exception as e:
        download = local_file_scanner(paths, 
                                        filenames,
                                        'nomads',
                                        run)       
    
    if download == True:
        print(f"Data downloading...")

        try:
            for path in paths:
                for file in os.listdir(f"{path}"):
                    os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        if cat != 'members':
            for path in paths:
                for url, filename in zip(urls, filenames):
                    client.get_gridded_data(f"{url}",
                                path,
                                f"{filename}.grib2",
                                proxies=proxies,
                                chunk_size=chunk_size,
                                notifications=notifications)    
        else:
            start = 0
            increment = int(len(filenames)/len(members))
            stop = increment
            for path in paths:
                for u, f in zip(range(start, stop, 1), range(start, stop, 1)):
                    client.get_gridded_data(f"{urls[u]}",
                                path,
                                f"{filenames[f]}.grib2",
                                proxies=proxies,
                                chunk_size=chunk_size,
                                notifications=notifications)   
                                
                start = start + increment
                stop = stop + increment            
        print(f"Download Complete.")        
    else:
        print(f"User has the current dataset.\nSkipping download.")
        
    if process_data == True:
        print(f"Data Processing...")
        
        clear_empty_files(paths)
        
        ds = process_gefs_data('gefs0p25', 
                                    cat,
                                    members)
        
        if convert_temperature == True:
            ds = convert_temperature_units(ds, 
                                           convert_to,
                                           cat=cat)
                
        clear_idx_files('gefs0p25', 
                    cat, 
                    members)
        
        print(f"Data Processing Complete.")
        return ds
    else:
        pass