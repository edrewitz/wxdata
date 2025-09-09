"""
This file hosts functions that download various types of GFS and GEFS Data

(C) Eric J. Drewitz 2025
"""


import xarray as xr
import numpy as np
import urllib.request
import os
import sys
import logging
import glob
import warnings
warnings.filterwarnings('ignore')

from wxdata.scanners.url_scanners import gfs_url_scanner
from wxdata.scanners.file_scanners import file_scanner

from wxdata.utils.file_funcs import(
    
    ens_folders, 
    clear_idx_files    
)

from wxdata.gfs.process import process_data

from wxdata.utils.recycle_bin import *
clear_recycle_bin_windows()
clear_trash_bin_mac()
clear_trash_bin_linux()

try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta

try:
    utc_time = datetime.now(UTC)
except Exception as e:
    utc_time = datetime.utcnow()

local_time = datetime.now()

yesterday = utc_time - timedelta(hours=24)

def gefs_0p50(cat, step=3, western_bound=-180, eastern_bound=180, northern_bound=90, southern_bound=-90, proxies=None, directory='atmos', members='all', final_forecast_hour=384):

    """
    This function retrives the latest GEFS0P50 data. If the data is not previously downloaded nor up to date, the function
    will download and pre-process the latest dataset. 

    To avoid bans from the data servers, the function will scan the data server and locally hosted files and if the 
    files are up to date, the function will skip downloading the newest dataset. 

    Required Arguments:

    1) cat (String) - The category of the data. (i.e. mean, control, members)

    Optional Arguments:
    
    1) step (Integer) - Default = 3. The hourly increments of the dataset. Valid step intervals are 3hr and 6hr.  

    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    6) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }

    7) directory (String) - Default='atmos'. The directory the user wants to download data from.
       Directories: 1) atmos
                    2) chem
                    
    8) members (String or List) - Default = 'all'. The individual ensemble members. There are 30 members in this ensemble.
    If 'all' is selected, all 30 members will download. This could be timeconsuming so if the user wishes to only use a select number
    of members, the user must pass in a list of integers corresponding to the ensemble members. 
    
    Here is an example: I would like to download the first 5 ensemble members ----> set members=[1, 2, 3, 4, 5]
    
    *CAT MUST BE SET TO 'members' FOR THIS ARGUMENT TO BE VALID*
    
    9) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    Here is an example: I want to only download and parse up to 240 hours which is 7 days ----> set final_forecast_hour=240   
    

    Returns
    -------

    A processed xarray.data array of the latest GEFS0P50 data. 
    
    wxdata converts all GRIB variable keys into a standardized variable key format that is in plain language. 
    
    New Variable Keys After Pre-Processing (Decrypted GRIB Keys Into Plain Language)
    --------------------------------------------------------------------------------
    
    ATMOS (Atmospheric) Directory
    -----------------------------

        'surface_pressure'
        'orography'
        'water_equivalent_of_accumulated_snow_depth'
        'snow_depth'
        'sea_ice_thickness'
        'total_precipitation'
        'categorical_snow'
        'categorical_ice_pellets'
        'categorical_freezing_rain'
        'categorical_rain'] = 'crain'
        'time_mean_surface_latent_heat_flux'
        'time_mean_surface_sensible_heat_flux'
        'surface_downward_shortwave_radiation_flux'
        'surface_downward_longwave_radiation_flux'
        'surface_upward_shortwave_radiation_flux'
        'surface_upward_longwave_radiation_flux'
        'mslp'
        'soil_temperature'
        'soil_moisture'
        '2m_relative_humidity'
        '2m_temperature'
        'maximum_temperature'
        'minimum_temperature'
        'precipitable_water'
        'geopotential_height'
        'air_temperature'
        'relative_humidity'
        'u_wind_component'
        'v_wind_component'
        'mixed_layer_cape'
        'mixed_layer_cin'
        

    CHEM (Atmospheric Chemistry) Directory
    --------------------------------------
    
        'fine_particulates'
        'coarse_particulates'
                          
    """  
    sys.tracebacklimit = 0
    logging.disable()
    cat = cat.upper()
    model = 'GEFS0P50'
    if final_forecast_hour > 384:
        final_forecast_hour = 384
    
    if step == 6:
        if final_forecast_hour > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = final_forecast_hour + step
    elif step == 3:
        if final_forecast_hour > 100:
            step = 3
            stop = 99 + step
            start = 102
        else:
            step = 3
            stop = final_forecast_hour + step
    else:
        print("ERROR! User entered an invalid step value\nSteps must either be 3 or 6 hourly.")
        sys.exit(1)

    if cat == 'MEAN' or cat == 'CONTROL':
        clear_idx_files(directory=directory, step=step, model=model, cat=cat)
        url, run = gfs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour)
        download = file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour)
        directory = directory.upper()
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        else:
            run = run
            
        if cat == 'MEAN':
            ff = 'avg'
        if cat == 'CONTROL':
            ff = 'c00'
        if download == True:
            print(f"Downloading the latest {model} data...")
    
            for file in os.listdir(f"{model}/{cat}/{step}/{directory}"):
                try:
                    os.remove(f"{model}/{cat}/{step}/{directory}/{file}")
                except Exception as e:
                    pass
                
            if directory == 'ATMOS':
            
                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2a.0p50.f00{i}", f"ge{ff}.t{run}z.pgrb2a.0p50.f00{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2a.0p50.f00{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50.f00{i}")
                    else:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2a.0p50.f0{i}", f"ge{ff}.t{run}z.pgrb2a.0p50.f0{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2a.0p50.f0{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50.f0{i}")
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2a.0p50.f{i}", f"ge{ff}.t{run}z.pgrb2a.0p50.f{i}")
                            os.replace(f"ge{ff}.t{run}z.pgrb2a.0p50.f{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50.f{i}") 
                        except Exception as e:
                            pass 

                for i in range(0, stop, step):
                    if i < 10:
                        try:
                            os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50.f00{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50_f00{i}.grib2")
                        except Exception as e:
                            pass
                    else:
                        try:
                            os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50.f0{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50_f0{i}.grib2")
                        except Exception as e:
                            pass
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50.f{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2a.0p50_f{i}.grib2")
                        except Exception as e:
                            pass    
                        
            else:
                
                if final_forecast_hour >= 120:
                    final_forecast_hour = 120
                    
                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}gefs.chem.t{run}z.a3d_0p50.f00{i}.grib2", f"gefs.chem.t{run}z.a3d_0p50.f00{i}.grib2")
                        os.replace(f"gefs.chem.t{run}z.a3d_0p50.f00{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.chem.t{run}z.a3d_0p50.f00{i}.grib2")
                    else:
                        urllib.request.urlretrieve(f"{url}gefs.chem.t{run}z.a3d_0p50.f0{i}.grib2", f"gefs.chem.t{run}z.a3d_0p50.f0{i}.grib2")
                        os.replace(f"gefs.chem.t{run}z.a3d_0p50.f0{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.chem.t{run}z.a3d_0p50.f0{i}.grib2")
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}gefs.chem.t{run}z.a3d_0p50.f{i}.grib2", f"gefs.chem.t{run}z.a3d_0p50.f{i}.grib2")
                            os.replace(f"gefs.chem.t{run}z.a3d_0p50.f{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.chem.t{run}z.a3d_0p50.f{i}.grib2") 
                        except Exception as e:
                            pass              

        else:
            print(f"Data in f:{model}/{cat}/{step} is current. Skipping download.")
        
        ds = process_data(model, cat, step, directory, western_bound, eastern_bound, northern_bound, southern_bound, False)

        clear_idx_files(directory=directory, step=step, model=model, cat=cat)

    else:
        
        try:
            members = members.lower()
        except Exception as e:
            pass
        
        try:
            if members == 'all':
                members = np.arange(0, 31, 1)
            else:
                members = members
        except Exception as e:
            members = members
            
        paths = ens_folders(model, cat, step, directory, members)
        clear_idx_files(paths=paths, ens=True)
        url, run = gfs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour, members=members)
        download = file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour, ens_members=True, members=members)
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        else:
            run = run

        if download == True:
            print(f"Downloading the latest {model} data...")
            for pp in paths:
                for file in os.listdir(f"{pp}"):
                    try:
                        os.remove(f"{pp}/{file}")
                    except Exception as e:
                        pass            

            for e, p in zip(members, paths):
                if e < 10:
                    ff = f"p0{e}"
                else:
                    ff = f"p{e}"
                        
                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2a.0p50.f00{i}", f"ge{ff}.t{run}z.pgrb2a.0p50.f00{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2a.0p50.f00{i}", f"{p}/ge{ff}.t{run}z.pgrb2a.0p50.f00{i}")
                    else:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2a.0p50.f0{i}", f"ge{ff}.t{run}z.pgrb2a.0p50.f0{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2a.0p50.f0{i}", f"{p}/ge{ff}.t{run}z.pgrb2a.0p50.f0{i}")
                        
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2a.0p50.f{i}", f"ge{ff}.t{run}z.pgrb2a.0p50.f{i}")
                            os.replace(f"ge{ff}.t{run}z.pgrb2a.0p50.f{i}", f"{p}/ge{ff}.t{run}z.pgrb2a.0p50.f{i}")  
                        except Exception as e:
                            pass
                            
                for i in range(0, stop, step):
                    if i < 10:
                        try:
                            os.replace(f"{p}/ge{ff}.t{run}z.pgrb2a.0p50.f00{i}", f"{p}/ge{ff}.t{run}z.pgrb2a.0p50_f00{i}.grib2")
                        except Exception as e:
                            pass
                    else:
                        try:
                            os.replace(f"{p}/ge{ff}.t{run}z.pgrb2a.0p50.f0{i}", f"{p}/ge{ff}.t{run}z.pgrb2a.0p50_f0{i}.grib2")
                        except Exception as e:
                            pass
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            os.replace(f"{p}/ge{ff}.t{run}z.pgrb2a.0p50.f{i}", f"{p}/ge{ff}.t{run}z.pgrb2a.0p50_f{i}.grib2")
                        except Exception as e:
                            pass    

        else:
            print(f"Data in f:{model}/{cat} is current. Skipping download.")

        ds = process_data(model, cat, step, directory, western_bound, eastern_bound, northern_bound, southern_bound, True)
        clear_idx_files(paths=paths, ens=True)
        
    return ds


def gefs_0p50_secondary_parameters(cat, step=3, western_bound=-180, eastern_bound=180, northern_bound=90, southern_bound=-90, proxies=None, members='all', final_forecast_hour=384):

    """
    This function retrives the latest GEFS0P50 SECONDARY PARAMETERS data. If the data is not previously downloaded nor up to date, the function
    will download and pre-process the latest dataset. 

    To avoid bans from the data servers, the function will scan the data server and locally hosted files and if the 
    files are up to date, the function will skip downloading the newest dataset. 

    Required Arguments:

    1) cat (String) - The category of the data. (i.e. mean, control, members)

    Optional Arguments:
    
    1) step (Integer) - Default = 3. The hourly increments of the dataset. Valid step intervals are 3hr and 6hr.  

    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    6) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
                    
    7) members (String or List) - Default = 'all'. The individual ensemble members. There are 30 members in this ensemble.
    If 'all' is selected, all 30 members will download. This could be timeconsuming so if the user wishes to only use a select number
    of members, the user must pass in a list of integers corresponding to the ensemble members. 
    
    Here is an example: I would like to download the first 5 ensemble members ----> set members=[1, 2, 3, 4, 5]
    
    *CAT MUST BE SET TO 'members' FOR THIS ARGUMENT TO BE VALID*
    
    8) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    Here is an example: I want to only download and parse up to 240 hours which is 7 days ----> set final_forecast_hour=240   
    

    Returns
    -------

    A processed xarray.data array of the latest GEFS0P50 SECONDARY PARAMETERS data. 
    
    wxdata converts all GRIB variable keys into a standardized variable key format that is in plain language. 
    
    New Variable Keys After Pre-Processing (Decrypted GRIB Keys Into Plain Language)
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
    sys.tracebacklimit = 0
    logging.disable()
    cat = cat.upper()
    model = 'GEFS0P50 SECONDARY PARAMETERS'
    directory = 'atmos'
    if final_forecast_hour > 384:
        final_forecast_hour = 384
    
    if cat == 'MEAN':
        cat = 'CONTROL'
    
    if step == 6:
        if final_forecast_hour > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = final_forecast_hour + step
    elif step == 3:
        if final_forecast_hour > 100:
            step = 3
            stop = 99 + step
            start = 102
        else:
            step = 3
            stop = final_forecast_hour + step
    else:
        print("ERROR! User entered an invalid step value\nSteps must either be 3 or 6 hourly.")
        sys.exit(1)

    if cat == 'CONTROL':
        clear_idx_files(directory=directory, step=step, model=model, cat=cat)
        url, run = gfs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour)
        download = file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour)
        directory = directory.upper()
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        else:
            run = run
            
        if cat == 'CONTROL':
            ff = 'c00'
        if download == True:
            print(f"Downloading the latest {model} data...")
    
            for file in os.listdir(f"{model}/{cat}/{step}/{directory}"):
                try:
                    os.remove(f"{model}/{cat}/{step}/{directory}/{file}")
                except Exception as e:
                    pass
            
            for i in range(0, stop, step):
                if i < 10:
                    urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2b.0p50.f00{i}", f"ge{ff}.t{run}z.pgrb2b.0p50.f00{i}")
                    os.replace(f"ge{ff}.t{run}z.pgrb2b.0p50.f00{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50.f00{i}")
                else:
                    urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2b.0p50.f0{i}", f"ge{ff}.t{run}z.pgrb2b.0p50.f0{i}")
                    os.replace(f"ge{ff}.t{run}z.pgrb2b.0p50.f0{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50.f0{i}")
            if final_forecast_hour > 100:
                for i in range(start, final_forecast_hour + step, step):
                    try:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2b.0p50.f{i}", f"ge{ff}.t{run}z.pgrb2b.0p50.f{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2b.0p50.f{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50.f{i}") 
                    except Exception as e:
                        pass 

            for i in range(0, stop, step):
                if i < 10:
                    try:
                        os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50.f00{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50_f00{i}.grib2")
                    except Exception as e:
                        pass
                else:
                    try:
                        os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50.f0{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50_f0{i}.grib2")
                    except Exception as e:
                        pass
            if final_forecast_hour > 100:
                for i in range(start, final_forecast_hour + step, step):
                    try:
                        os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50.f{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2b.0p50_f{i}.grib2")
                    except Exception as e:
                        pass    
                        

        else:
            print(f"Data in f:{model}/{cat}/{step} is current. Skipping download.")
        
        ds = process_data(model, cat, step, directory, western_bound, eastern_bound, northern_bound, southern_bound, False)

        clear_idx_files(directory=directory, step=step, model=model, cat=cat)

    else:
        
        try:
            members = members.lower()
        except Exception as e:
            pass
        
        try:
            if members == 'all':
                members = np.arange(0, 31, 1)
            else:
                members = members
        except Exception as e:
            members = members
            
        paths = ens_folders(model, cat, step, directory, members)
        clear_idx_files(paths=paths, ens=True)
        url, run = gfs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour, members=members)
        download = file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour, ens_members=True, members=members)
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        else:
            run = run

        if download == True:
            print(f"Downloading the latest {model} data...")
            for pp in paths:
                for file in os.listdir(f"{pp}"):
                    try:
                        os.remove(f"{pp}/{file}")
                    except Exception as e:
                        pass            

            for e, p in zip(members, paths):
                if e < 10:
                    ff = f"p0{e}"
                else:
                    ff = f"p{e}"
                        
                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2b.0p50.f00{i}", f"ge{ff}.t{run}z.pgrb2b.0p50.f00{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2b.0p50.f00{i}", f"{p}/ge{ff}.t{run}z.pgrb2b.0p50.f00{i}")
                    else:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2b.0p50.f0{i}", f"ge{ff}.t{run}z.pgrb2b.0p50.f0{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2b.0p50.f0{i}", f"{p}/ge{ff}.t{run}z.pgrb2b.0p50.f0{i}")
                        
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2b.0p50.f{i}", f"ge{ff}.t{run}z.pgrb2b.0p50.f{i}")
                            os.replace(f"ge{ff}.t{run}z.pgrb2b.0p50.f{i}", f"{p}/ge{ff}.t{run}z.pgrb2b.0p50.f{i}")  
                        except Exception as e:
                            pass
                            
                for i in range(0, stop, step):
                    if i < 10:
                        try:
                            os.replace(f"{p}/ge{ff}.t{run}z.pgrb2b.0p50.f00{i}", f"{p}/ge{ff}.t{run}z.pgrb2b.0p50_f00{i}.grib2")
                        except Exception as e:
                            pass
                    else:
                        try:
                            os.replace(f"{p}/ge{ff}.t{run}z.pgrb2b.0p50.f0{i}", f"{p}/ge{ff}.t{run}z.pgrb2b.0p50_f0{i}.grib2")
                        except Exception as e:
                            pass
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            os.replace(f"{p}/ge{ff}.t{run}z.pgrb2b.0p50.f{i}", f"{p}/ge{ff}.t{run}z.pgrb2b.0p50_f{i}.grib2")
                        except Exception as e:
                            pass    

        else:
            print(f"Data in f:{model}/{cat} is current. Skipping download.")

        ds = process_data(model, cat, step, directory, western_bound, eastern_bound, northern_bound, southern_bound, True)
        clear_idx_files(paths=paths, ens=True)
        
    return ds



def gefs_0p25(cat, step=3, u_and_v_wind=False, western_bound=-180, eastern_bound=180, northern_bound=90, southern_bound=-90, proxies=None, directory='atmos', members='all', final_forecast_hour=384):

    """
    This function retrives the latest GEFS0P25 data. If the data is not previously downloaded nor up to date, the function
    will download and pre-process the latest dataset. 

    To avoid bans from the data servers, the function will scan the data server and locally hosted files and if the 
    files are up to date, the function will skip downloading the newest dataset. 

    Required Arguments:

    1) cat (String) - The category of the data. (i.e. mean, control, members, (prob, spread -> only if directory='wave'))

    Optional Arguments:
    
    1) step (Integer) - Default = 3. The hourly increments of the dataset. Valid step intervals are 3hr and 6hr.  

    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    6) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }

    7) directory (String) - Default='atmos'. The directory the user wants to download data from.
       Directories: 1) atmos
                    2) chem
                    3) wave
                    
    8) members (String or List) - Default = 'all'. The individual ensemble members. There are 30 members in this ensemble.
    If 'all' is selected, all 30 members will download. This could be timeconsuming so if the user wishes to only use a select number
    of members, the user must pass in a list of integers corresponding to the ensemble members. 
    
    Here is an example: I would like to download the first 5 ensemble members ----> set members=[1, 2, 3, 4, 5]
    
    *CAT MUST BE SET TO 'members' FOR THIS ARGUMENT TO BE VALID*
    
    9) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    Here is an example: I want to only download and parse up to 240 hours which is 7 days ----> set final_forecast_hour=240   
    

    Returns
    -------

    A processed xarray.data array of the latest GEFS0P25 data. 
    
    wxdata converts all GRIB variable keys into a standardized variable key format that is in plain language. 
    
    New Variable Keys After Pre-Processing (Decrypted GRIB Keys Into Plain Language)
    --------------------------------------------------------------------------------
    
        ATMOS (Atmospheric) Directory
        -----------------------------
          
            'surface_visibility'
            'surface_wind_gust'
            'surface_pressure'
            'orography'
            'water_equivalent_of_accumulated_snow_depth'
            'snow_depth'
            'sea_ice_thickness'
            'percent_frozen_precipitation'
            'surface_cape'
            'surface_cin'
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
            'mslp'
            'mslp_eta_reduction' 
            'soil_temperature'
            'soil_moisture'
            '2m_relative_humidity'
            '2m_temperature'
            '2m_dew_point'
            'maximum_temperature'
            'minimum_temperature'           
            '10m_u_wind_component'
            '10m_v_wind_component'
            'precipitable_water'
            'cloud_ceiling_height'    
            '3km_helicity'     
            'mixed_layer_cape'
            'mixed_layer_cin'    
            
        CHEM (Atmospheric Chemistry) Directory
        --------------------------------------
        
            'fine_particulates'
            'coarse_particulates'    
    
    
        WAVE (Marine Weather/Ocean Forecasting)
        ---------------------------------------
        
            'significant_wave_height_combined_wind_waves_and_swell'
            'primary_wave_period'
            'primary_wave_direction'
            'significant_wave_height_wind_waves'
            'wind_wave_mean_period'
            'wind_wave_direction'
            'wind_speed'
            'wind_direction'
            'significant_height_of_total_swell'
            'mean_period_of_total_swell'
            'direction_of_swell_waves'
            'u_wind_component'
            'v_wind_component'
            'sea_ice_area_fraction'
            'mean_wave_period_based_on_first_moment'
            'mean_wave_period'
            'mean_wave_direction' 
                          
    """  
    sys.tracebacklimit = 0
    logging.disable()
    cat = cat.upper()
    model = 'GEFS0P25'
    directory = directory.lower()
    
    if final_forecast_hour > 240 and directory != 'wave':
        final_forecast_hour = 240
    else:
        final_forecast_hour = final_forecast_hour
        if final_forecast_hour > 384:
            final_forecast_hour = 384
        else:
            final_forecast_hour = final_forecast_hour
    
    if step == 6:
        if final_forecast_hour > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = final_forecast_hour + step
    elif step == 3:
        if final_forecast_hour > 100:
            step = 3
            stop = 99 + step
            start = 102
        else:
            step = 3
            stop = final_forecast_hour + step
    else:
        print("ERROR! User entered an invalid step value\nSteps must either be 3 or 6 hourly.")
        sys.exit(1)

    if cat == 'MEAN' or cat == 'CONTROL' or cat == 'SPREAD' or cat == 'PROB':
        clear_idx_files(directory=directory, step=step, model=model, cat=cat)
        url, run = gfs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour)
        download = file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour)
        directory = directory.upper()
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        else:
            run = run
            
        if cat == 'MEAN':
            ff = 'avg'
        if cat == 'CONTROL':
            ff = 'c00'
        if download == True:
            print(f"Downloading the latest {model} data...")
    
            for file in os.listdir(f"{model}/{cat}/{step}/{directory}"):
                try:
                    os.remove(f"{model}/{cat}/{step}/{directory}/{file}")
                except Exception as e:
                    pass
                
            if directory == 'ATMOS':
                
                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f00{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}")
                    else:
                        urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f0{i}")
                        os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}")
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f{i}")
                            os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}") 
                        except Exception as e:
                            pass 

                for i in range(0, stop, step):
                    if i < 10:
                        try:
                            os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25_f00{i}.grib2")
                        except Exception as e:
                            pass
                    else:
                        try:
                            os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25_f0{i}.grib2")
                        except Exception as e:
                            pass
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            os.replace(f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"{model}/{cat}/{step}/{directory}/ge{ff}.t{run}z.pgrb2s.0p25_f{i}.grib2")
                        except Exception as e:
                            pass    
                        
            elif directory == 'CHEM':
                
                if final_forecast_hour >= 120:
                    final_forecast_hour = 120
                    
                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}gefs.chem.t{run}z.a2d_0p25.f00{i}.grib2", f"gefs.chem.t{run}z.a2d_0p25.f00{i}.grib2")
                        os.replace(f"gefs.chem.t{run}z.a2d_0p25.f00{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.chem.t{run}z.a2d_0p25.f00{i}.grib2")
                    else:
                        urllib.request.urlretrieve(f"{url}gefs.chem.t{run}z.a2d_0p25.f0{i}.grib2", f"gefs.chem.t{run}z.a2d_0p25.f0{i}.grib2")
                        os.replace(f"gefs.chem.t{run}z.a2d_0p25.f0{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.chem.t{run}z.a2d_0p25.f0{i}.grib2")
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}gefs.chem.t{run}z.a2d_0p25.f{i}.grib2", f"gefs.chem.t{run}z.a2d_0p25.f{i}.grib2")
                            os.replace(f"gefs.chem.t{run}z.a2d_0p25.f{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.chem.t{run}z.a2d_0p25.f{i}.grib2") 
                        except Exception as e:
                            pass 
                        
            else:
                cat = cat.lower()
                if cat == 'control':
                    ct = 'c00'
                else:
                    ct = cat.lower()

                for i in range(0, stop, step):
                    if i < 10:
                        urllib.request.urlretrieve(f"{url}gefs.wave.t{run}z.{ct}.global.0p25.f00{i}.grib2", f"gefs.wave.t{run}z.{ct}.global.0p25.f00{i}.grib2")
                        os.replace(f"gefs.wave.t{run}z.{ct}.global.0p25.f00{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.wave.t{run}z.{cat}.global.0p25.f00{i}.grib2")
                    else:
                        urllib.request.urlretrieve(f"{url}gefs.wave.t{run}z.{ct}.global.0p25.f0{i}.grib2", f"gefs.wave.t{run}z.{ct}.global.0p25.f0{i}.grib2")
                        os.replace(f"gefs.wave.t{run}z.{ct}.global.0p25.f0{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.wave.t{run}z.{cat}.global.0p25.f0{i}.grib2")
                if final_forecast_hour > 100:
                    for i in range(start, final_forecast_hour + step, step):
                        try:
                            urllib.request.urlretrieve(f"{url}gefs.wave.t{run}z.{ct}.global.0p25.f{i}.grib2", f"gefs.wave.t{run}z.{ct}.global.0p25.f{i}.grib2")
                            os.replace(f"gefs.wave.t{run}z.{ct}.global.0p25.f{i}.grib2", f"{model}/{cat}/{step}/{directory}/gefs.wave.t{run}z.{cat}.global.0p25.f{i}.grib2") 
                        except Exception as e:
                            pass 
                  

            

        else:
            print(f"Data in f:{model}/{cat}/{step} is current. Skipping download.")
        
        ds = process_data(model, cat, step, directory, western_bound, eastern_bound, northern_bound, southern_bound, False)

        clear_idx_files(directory=directory, step=step, model=model, cat=cat)

    else:
        
        try:
            members = members.lower()
        except Exception as e:
            pass
        
        try:
            if members == 'all':
                members = np.arange(0, 31, 1)
            else:
                members = members
        except Exception as e:
            members = members
            
        paths = ens_folders(model, cat, step, directory, members)
        clear_idx_files(paths=paths, ens=True)
        url, run = gfs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour, members=members)
        download = file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour, ens_members=True, members=members)
        if run == 0:
            run = '00'
        elif run == 6:
            run = '06'
        else:
            run = run

        if download == True:
            print(f"Downloading the latest {model} data...")
            for pp in paths:
                for file in os.listdir(f"{pp}"):
                    try:
                        os.remove(f"{pp}/{file}")
                    except Exception as e:
                        pass            

            for e, p in zip(members, paths):
                if e < 10:
                    ff = f"p0{e}"
                else:
                    ff = f"p{e}"
                        
                if directory == 'ATMOS':
                    for i in range(0, stop, step):
                        if i < 10:
                            urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f00{i}")
                            os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"{p}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}")
                        else:
                            urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f0{i}")
                            os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"{p}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}")
                            
                    if final_forecast_hour > 100:
                        for i in range(start, final_forecast_hour + step, step):
                            try:
                                urllib.request.urlretrieve(f"{url}ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"ge{ff}.t{run}z.pgrb2s.0p25.f{i}")
                                os.replace(f"ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"{p}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}")  
                            except Exception as e:
                                pass
                                
                    for i in range(0, stop, step):
                        if i < 10:
                            try:
                                os.replace(f"{p}/ge{ff}.t{run}z.pgrb2s.0p25.f00{i}", f"{p}/ge{ff}.t{run}z.pgrb2s.0p25_f00{i}.grib2")
                            except Exception as e:
                                pass
                        else:
                            try:
                                os.replace(f"{p}/ge{ff}.t{run}z.pgrb2s.0p25.f0{i}", f"{p}/ge{ff}.t{run}z.pgrb2s.0p25_f0{i}.grib2")
                            except Exception as e:
                                pass
                    if final_forecast_hour > 100:
                        for i in range(start, final_forecast_hour + step, step):
                            try:
                                os.replace(f"{p}/ge{ff}.t{run}z.pgrb2s.0p25.f{i}", f"{p}/ge{ff}.t{run}z.pgrb2s.0p25_f{i}.grib2")
                            except Exception as e:
                                pass    
                            
                else:
                    
                    for i in range(0, stop, step):
                        if i < 10:
                            urllib.request.urlretrieve(f"{url}gefs.wave.t{run}z.{ff}.global.0p25.f00{i}.grib2", f"gefs.wave.t{run}z.{ff}.global.0p25.f00{i}.grib2")
                            os.replace(f"gefs.wave.t{run}z.{ff}.global.0p25.f00{i}.grib2", f"{p}/gefs.wave.t{run}z.{ff}.global.0p25.f00{i}.grib2")
                        else:
                            urllib.request.urlretrieve(f"{url}gefs.wave.t{run}z.{ff}.global.0p25.f0{i}.grib2", f"gefs.wave.t{run}z.{ff}.global.0p25.f0{i}.grib2")
                            os.replace(f"gefs.wave.t{run}z.{ff}.global.0p25.f0{i}.grib2", f"{p}/gefs.wave.t{run}z.{ff}.global.0p25.f0{i}.grib2")
                            
                    if final_forecast_hour > 100:
                        for i in range(start, final_forecast_hour + step, step):
                            try:
                                urllib.request.urlretrieve(f"{url}gefs.wave.t{run}z.{ff}.global.0p25.f{i}.grib2", f"gefs.wave.t{run}z.{ff}.global.0p25.f{i}.grib2")
                                os.replace(f"gefs.wave.t{run}z.{ff}.global.0p25.f{i}.grib2", f"{p}/gefs.wave.t{run}z.{ff}.global.0p25.f{i}.grib2")  
                            except Exception as e:
                                pass
                                

        else:
            print(f"Data in f:{model}/{cat} is current. Skipping download.")

        ds = process_data(model, cat, step, directory, western_bound, eastern_bound, northern_bound, southern_bound, True)
        clear_idx_files(paths=paths, ens=True)
        
    return ds

            
