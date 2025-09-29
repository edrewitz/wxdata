def gefs_0p50_all_parameters(cat='mean', step=3, western_bound=-180, eastern_bound=180, northern_bound=90, southern_bound=-90, proxies=None, directory='atmos', members='all', final_forecast_hour=384):

    """
    This function retrives the latest GEFS0P50 data. If the data is not previously downloaded nor up to date, the function
    will download and pre-process the latest dataset. 

    To avoid bans from the data servers, the function will scan the data server and locally hosted files and if the 
    files are up to date, the function will skip downloading the newest dataset. 

    Required Arguments: None

    Optional Arguments:
    
    1) cat (String) - Default='mean'. The category of the data. (i.e. mean, control, members)
    
    2) step (Integer) - Default = 3. The hourly increments of the dataset. Valid step intervals are 3hr and 6hr.  

    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    7) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }

    8) directory (String) - Default='atmos'. The directory the user wants to download data from.
       Directories: 1) atmos
                    2) chem
                    
    9) members (String or List) - Default = 'all'. The individual ensemble members. There are 30 members in this ensemble.
    If 'all' is selected, all 30 members will download. This could be timeconsuming so if the user wishes to only use a select number
    of members, the user must pass in a list of integers corresponding to the ensemble members. 
    
    Here is an example: I would like to download the first 5 ensemble members ----> set members=[1, 2, 3, 4, 5]
    
    *CAT MUST BE SET TO 'members' FOR THIS ARGUMENT TO BE VALID*
    
    10) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
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
        'categorical_rain'
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
    
    wlon = convert_lon(western_bound)
    elon = convert_lon(eastern_bound)
    
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
        url, run = gefs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour)
        download = gfs_file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour)
        directory = directory.upper()
        
        date = gefs_url_date_index(url)
        
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
                        
                        url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl?"
                                    f"dir=%2Fgefs.{date}%2F18%2F{directory}%2Fpgrb2ap5&file=geavg.t18z.pgrb2a.0p50.f000&all_var=on&all_lev=on&"
                                    f"subregion=&toplat=90&leftlon=0&rightlon=360&bottomlat=-90")
                        
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
        url, run = gefs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour, members=members)
        download = gfs_file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour, ens_members=True, members=members)
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


def gefs_0p50_secondary_parameters_full(cat='control', step=3, western_bound=-180, eastern_bound=180, northern_bound=90, southern_bound=-90, proxies=None, members='all', final_forecast_hour=384):

    """
    This function retrives the latest GEFS0P50 SECONDARY PARAMETERS data. If the data is not previously downloaded nor up to date, the function
    will download and pre-process the latest dataset. 

    To avoid bans from the data servers, the function will scan the data server and locally hosted files and if the 
    files are up to date, the function will skip downloading the newest dataset. 

    Required Arguments: None

    Optional Arguments:
    
    1) cat (String) - Default='control' The category of the data. (i.e. mean, control, members)
    *If the user sets cat='mean', cat will automatically be reset to 'control' as mean is not valid for this dataset*
    
    2) step (Integer) - Default = 3. The hourly increments of the dataset. Valid step intervals are 3hr and 6hr.  

    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    7) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }
                    
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
        url, run = gefs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour)
        download = gfs_file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour)
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
        url, run = gefs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour, members=members)
        download = gfs_file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour, ens_members=True, members=members)
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



def gefs_0p25_full(cat='mean', step=3, u_and_v_wind=False, western_bound=-180, eastern_bound=180, northern_bound=90, southern_bound=-90, proxies=None, directory='atmos', members='all', final_forecast_hour=384):

    """
    This function retrives the latest GEFS0P25 data. If the data is not previously downloaded nor up to date, the function
    will download and pre-process the latest dataset. 

    To avoid bans from the data servers, the function will scan the data server and locally hosted files and if the 
    files are up to date, the function will skip downloading the newest dataset. 

    Required Arguments: None
    
    Optional Arguments:
    
    1) cat (String) - Default='mean'. The category of the data. (i.e. mean, control, members, (prob, spread -> only if directory='wave'))
    
    2) step (Integer) - Default = 3. The hourly increments of the dataset. Valid step intervals are 3hr and 6hr.  

    3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    7) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }

    8) directory (String) - Default='atmos'. The directory the user wants to download data from.
       Directories: 1) atmos
                    2) chem
                    3) wave
                    
    9) members (String or List) - Default = 'all'. The individual ensemble members. There are 30 members in this ensemble.
    If 'all' is selected, all 30 members will download. This could be timeconsuming so if the user wishes to only use a select number
    of members, the user must pass in a list of integers corresponding to the ensemble members. 
    
    Here is an example: I would like to download the first 5 ensemble members ----> set members=[1, 2, 3, 4, 5]
    
    *CAT MUST BE SET TO 'members' FOR THIS ARGUMENT TO BE VALID*
    
    10) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
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
        url, run = gefs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour)
        download = gfs_file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour)
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
        url, run = gefs_url_scanner(f"{model}", f"{cat}", proxies, directory, final_forecast_hour, members=members)
        download = gfs_file_scanner(f"{model}", f"{cat}", directory, url, run, step, final_forecast_hour, ens_members=True, members=members)
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

 def gfs_file_scanner(model, cat, directory, url, url_run, step, final_forecast_hour, ens_members=False, members=None):

    """
    This function scans the directory to make sure: 
    
    1) The directory branch exists. 
    2) Builds the directory branch if it does not exist
    3) Makes sure the files are up to date

    Required Arguments: 

    1) model (String) - The model the user wants. 

    2) cat (String) - The category of data the user wants (i.e. ensmean vs. enscontrol). 

    3) url (String) - The URL returned from the url_scanner function. 

    4) url_run (Integer) - The model run time in the URL returned from the url_scanner function. 

    Returns
    -------

    1) A boolean value of True or False for download.
    """    
    model = model.upper()
    cat = cat.upper()
    directory = directory.upper()

    aa, bb = index(model, directory)
    
    if os.path.exists(f"{model}"):
        pass
    else:
        os.mkdir(f"{model}")

    if os.path.exists(f"{model}/{cat}"):
        pass
    else:
        os.mkdir(f"{model}/{cat}")

    if os.path.exists(f"{model}/{cat}/{step}"):
        pass
    else:
        os.mkdir(f"{model}/{cat}/{step}")
        
    if os.path.exists(f"{model}/{cat}/{step}/{directory}"):
        pass
    else:
        os.mkdir(f"{model}/{cat}/{step}/{directory}")      

    exists = False

    if ens_members == False:
        try:
            fnames = []
            for file in os.listdir(f"{model}/{cat}/{step}/{directory}"):
                fname = os.path.basename(f"{model}/{cat}/{step}/{directory}/{file}")
                fnames.append(fname)
            fname = fnames[-1]
            ftype = file_extension(fname)
            exists = True
        except Exception as e:
            download = True
        if exists == False:
            download = True
        else:
            file_run = int(f"{fname[aa]}{fname[bb]}")
            if file_run == url_run:
                modification_timestamp = os.path.getmtime(f"{model}/{cat}/{step}/{directory}/{fname}")
                readable_time = time.ctime(modification_timestamp)
                update_day = int(f"{readable_time[8]}{readable_time[9]}")
                update_hour = int(f"{readable_time[11]}{readable_time[12]}") 
                if update_day != local.day:
                    download = True
                else:
                    tdiff = local - timedelta(hours=6)
                    if update_hour < tdiff.hour:
                        download = True
                    else:
                        if ftype == False:
                            download = True
                        else:
                            download = file_fhour_checker(model, fname, final_forecast_hour)
                
            else:
                download = True

    else:
        members = members[-1]
        try:
            fnames = []
            for file in os.listdir(f"{model}/{cat}/{step}/{directory}/{members}"):
                fname = os.path.basename(f"{model}/{cat}/{step}/{directory}/{members}/{file}")
                fnames.append(fname)
            fname = fnames[-1]
            ftype = file_extension(fname)
            exists = True
        except Exception as e:
            download = True

        if exists == False:
            download = True
    
        else:
            file_run = int(f"{fname[aa]}{fname[bb]}")
            if file_run == url_run:
                modification_timestamp = os.path.getmtime(f"{model}/{cat}/{step}/{directory}/{members}/{fname}")
                readable_time = time.ctime(modification_timestamp)
                update_day = int(f"{readable_time[8]}{readable_time[9]}")
                update_hour = int(f"{readable_time[11]}{readable_time[12]}") 
                if update_day != local.day:
                    download = True
                else:
                    tdiff = local - timedelta(hours=6)
                    if update_hour < tdiff.hour:
                        download = True
                    else:
                        if ftype == False:
                            download = True
                        else:
                            download = file_fhour_checker(model, fname, final_forecast_hour)
                
            else:
                download = True
                    
        
    return download

def url_index(model, directory):

    """
    This function returns the string-index of the model run times in a file

    1) model (String) - The forecast model

    2) directory (String) - The directory the user wants to scan

    Optional Arguments: None

    Returns
    -------

    The index values of the run times in the file. 
    """
    
    if directory == 'atmos':
    
        times = {
            'GEFS0P25':[-19, -18],
            'GEFS0P50':[-18, -17],
            'GEFS0P50 SECONDARY PARAMETERS':[-18, -17],
            'GFS0P25':[-9, -8],
            'GFS0P25 SECONDARY PARAMETERS':[-9, -8]
        }
        
    elif directory == 'chem':

        times = {
            'GEFS0P25':[-18, -17],
            'GEFS0P50':[-17, -16],
            'GEFS0P50 SECONDARY PARAMETERS':[-17, -16],
            'GFS0P25':[-9, -8],
            'GFS0P25 SECONDARY PARAMETERS':[-9, -8]
        }
        
    else:
        
        times = {
            'GEFS0P25':[-16, -15],
            'GEFS0P50':[-16, -15],
            'GEFS0P50 SECONDARY PARAMETERS':[-16, -15],
            'GFS0P25':[-9, -8],
            'GFS0P25 SECONDARY PARAMETERS':[-9, -8]
        }        
        

    return times[model][0], times[model][1]


def index(model, directory):

    """
    This function returns the string-index of the model run times in a file

    1) model (String) - The forecast model

    Optional Arguments: None

    Returns
    -------

    The index values of the run times in the file. 
    """
    directory = directory.upper()
    
    if directory == 'ATMOS':
    
        times = {
            'GEFS0P25':[7, 8],
            'GEFS0P50':[7, 8],
            'GEFS0P50 SECONDARY PARAMETERS':[7, 8],
            'GFS0P25':[5, 6],
            'GFS0P25 SECONDARY PARAMETERS':[5, 6]
        }
        
    elif directory == 'CHEM':
        
        times = {
            'GEFS0P25':[7, 8],
            'GEFS0P50':[11, 12],
            'GFS0P25':[5, 6],
            'GFS0P25 SECONDARY PARAMETERS':[5, 6]
        }
    else:
        
        times = {
            'GEFS0P25':[11, 12],
            'GFS0P25':[5, 6],
            'GFS0P25 SECONDARY PARAMETERS':[5, 6]
        }

    return times[model][0], times[model][1]

def gfs_url_scanner():
    

    model = model.upper()
    cat = cat.upper()
    directory = directory.lower()
    
    if members != None:
        member = members[-1]
        if member < 10:
            member = f"0{member}"
        elif member >= 10:
            member = f"{member}"
        else:
            member = f"30"
    else:
        pass
    
    if model == 'GEFS0P25' and final_forecast_hour > 240:
        final_forecast_hour = 240
    
    if directory == 'chem' and final_forecast_hour >= 120:
        final_forecast_hour = 120
        
    if final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = final_forecast_hour

    try:
        aa, bb = url_index(model, directory)
    except Exception as e:
        print(f"{directory} is not a valid directory for {model}.")
        sys.exit(1)
    
    if directory == 'wave':
        folder = 'gridded'
    else:
        folder=''
    today_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/00/{directory}/{folder}"
    today_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/06/{directory}/{folder}"
    today_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/12/{directory}/{folder}"
    today_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{now.strftime('%Y%m%d')}/18/{directory}/{folder}"
    
    yday_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/00/{directory}/{folder}"
    yday_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/06/{directory}/{folder}"
    yday_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/12/{directory}/{folder}"
    yday_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{yd.strftime('%Y%m%d')}/18/{directory}/{folder}"
    
    if model == 'GFS0P25':
        f_00z = f"gfs.t00z.pgrb2.0p25.f{final_forecast_hour}"
        f_06z = f"gfs.t06z.pgrb2.0p25.f{final_forecast_hour}"
        f_12z = f"gfs.t12z.pgrb2.0p25.f{final_forecast_hour}"
        f_18z = f"gfs.t18z.pgrb2.0p25.f{final_forecast_hour}"
    else:
        f_00z = f"gfs.t00z.pgrb2b.0p25.f{final_forecast_hour}"
        f_06z = f"gfs.t06z.pgrb2b.0p25.f{final_forecast_hour}"
        f_12z = f"gfs.t12z.pgrb2b.0p25.f{final_forecast_hour}"
        f_18z = f"gfs.t18z.pgrb2b.0p25.f{final_forecast_hour}"


def gefs_url_scanner(model, cat, proxies, directory, final_forecast_hour, members=None):

    """
    This function scans https://nomads.ncep.noaa.gov/ for the file with the latest GEFS forecast model run. 
    If the page has complete data, the download link will be returned. 
    If the page is incomplete, the scanner will check for the previous run data.  

    Required Arguments: 

    1) model (String) - The model the user wants. 
    
    i) GEFS0P25
    ii) GEFS0P50
    iii) GEFS0P50 SECONDARY PARAMETERS

    2) cat (String) - The category of data the user wants (i.e. ensmean vs. enscontrol). 

    3) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                        }
                        
    4) directory (String) - The directory the user wants to scan.
       Directories: 1) atmos
                    2) chem
                    3) wave
                    
    5) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    Optional Arguments: 
    
    1) members (Integer) - Default = None. An array of integers corresponding to the last (highest number) ensemble member in the 
    datast which the user wishes to download. 

    Returns
    -------

    1) The download link.
    2) The time of the latest model run. 
    """
    model = model.upper()
    cat = cat.upper()
    directory = directory.lower()
    
    if members != None:
        member = members[-1]
        if member < 10:
            member = f"0{member}"
        elif member >= 10:
            member = f"{member}"
        else:
            member = f"30"
    else:
        pass
    
    if model == 'GEFS0P25' and final_forecast_hour > 240:
        final_forecast_hour = 240
    
    if directory == 'chem' and final_forecast_hour >= 120:
        final_forecast_hour = 120
        
    if final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = final_forecast_hour

    try:
        aa, bb = url_index(model, directory)
    except Exception as e:
        print(f"{directory} is not a valid directory for {model}.")
        sys.exit(1)
        
    if directory != 'wave':
        if model == 'GEFS0P25':
            
                if directory == 'atmos':
                    a = 's'
                else:
                    a = 'a'
                b = '25'
                c = '25'
            
        if model == 'GEFS0P50':
            a = 'a'
            b = '5'
            c = '50'

        if model == 'GEFS0P50 SECONDARY PARAMETERS':
            if directory == 'chem':
                a = 'a'
            else:
                a = 'b'
            b = '5'
            c = '50'
            
        folder = f"pgrb2{a}p{b}"
    else:
        if model == 'GEFS0P25':
            c = '25'
        if model == 'GEFS0P50' or model == 'GEFS0P50 SECONDARY PARAMETERS':
            c = '50'
        folder = 'gridded'

    today_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/00/{directory}/{folder}/"
    today_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/06/{directory}/{folder}/"
    today_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/12/{directory}/{folder}/"
    today_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{now.strftime('%Y%m%d')}/18/{directory}/{folder}/"
    
    yday_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/00/{directory}/{folder}/"
    yday_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/06/{directory}/{folder}/"
    yday_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/12/{directory}/{folder}/"
    yday_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yd.strftime('%Y%m%d')}/18/{directory}/{folder}/"

    if directory == 'atmos':
        if cat == 'MEAN':
            if model == 'GEFS0P50 SECONDARY PARAMETERS':
                f_00z = f"gec00.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_06z = f"gec00.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_12z = f"gec00.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_18z = f"gec00.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}" 
            elif model == 'GEFS0P50':
                f_00z = f"geavg.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_06z = f"geavg.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_12z = f"geavg.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_18z = f"geavg.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}"                
            else:
                f_00z = f"geavg.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_06z = f"geavg.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_12z = f"geavg.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_18z = f"geavg.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
        elif cat == 'CONTROL':
            if model == 'GEFS0P25':
                f_00z = f"gec00.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_06z = f"gec00.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_12z = f"gec00.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_18z = f"gec00.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}" 
            else:
                f_00z = f"gec00.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_06z = f"gec00.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_12z = f"gec00.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_18z = f"gec00.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}"                      
        else:
            if model == 'GEFS0P25':
                f_00z = f"gep{member}.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_06z = f"gep{member}.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_12z = f"gep{member}.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_18z = f"gep{member}.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}"   
            else:
                f_00z = f"gep{member}.t00z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_06z = f"gep{member}.t06z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_12z = f"gep{member}.t12z.pgrb2{a}.0p{c}.f{final_forecast_hour}"
                f_18z = f"gep{member}.t18z.pgrb2{a}.0p{c}.f{final_forecast_hour}"                         
    elif directory == 'chem':
        if model == 'GEFS0P25':
            f_00z = f"gefs.chem.t00z.a2d_0p{c}.f{final_forecast_hour}.grib2"    
            f_06z = f"gefs.chem.t06z.a2d_0p{c}.f{final_forecast_hour}.grib2"  
            f_12z = f"gefs.chem.t12z.a2d_0p{c}.f{final_forecast_hour}.grib2"  
            f_18z = f"gefs.chem.t18z.a2d_0p{c}.f{final_forecast_hour}.grib2"   
        else:
            f_00z = f"gefs.chem.t00z.a3d_0p{c}.f{final_forecast_hour}.grib2"    
            f_06z = f"gefs.chem.t06z.a3d_0p{c}.f{final_forecast_hour}.grib2"  
            f_12z = f"gefs.chem.t12z.a3d_0p{c}.f{final_forecast_hour}.grib2"  
            f_18z = f"gefs.chem.t18z.a3d_0p{c}.f{final_forecast_hour}.grib2"   
    else:
        if cat == 'MEAN' or cat == 'SPREAD' or cat == 'PROB':
            f_00z = f"gefs.wave.t00z.{cat.lower()}.global.0p{c}.f{final_forecast_hour}.grib2"  
            f_06z = f"gefs.wave.t06z.{cat.lower()}.global.0p{c}.f{final_forecast_hour}.grib2"  
            f_12z = f"gefs.wave.t12z.{cat.lower()}.global.0p{c}.f{final_forecast_hour}.grib2"  
            f_18z = f"gefs.wave.t18z.{cat.lower()}.global.0p{c}.f{final_forecast_hour}.grib2"  
        elif cat == 'CONTROL':
            f_00z = f"gefs.wave.t00z.c00.global.0p{c}.f{final_forecast_hour}.grib2"  
            f_06z = f"gefs.wave.t06z.c00.global.0p{c}.f{final_forecast_hour}.grib2"  
            f_12z = f"gefs.wave.t12z.c00.global.0p{c}.f{final_forecast_hour}.grib2"  
            f_18z = f"gefs.wave.t18z.c00.global.0p{c}.f{final_forecast_hour}.grib2"  
        else:
            f_00z = f"gefs.wave.t00z.p{member}.global.0p{c}.f{final_forecast_hour}.grib2"  
            f_06z = f"gefs.wave.t06z.p{member}.global.0p{c}.f{final_forecast_hour}.grib2"  
            f_12z = f"gefs.wave.t12z.p{member}.global.0p{c}.f{final_forecast_hour}.grib2"  
            f_18z = f"gefs.wave.t18z.p{member}.global.0p{c}.f{final_forecast_hour}.grib2"     
                                         
    if proxies == None:
        t_18z = requests.get(f"{today_18z}{f_18z}", stream=True)
        t_12z = requests.get(f"{today_12z}{f_12z}", stream=True)
        t_06z = requests.get(f"{today_06z}{f_06z}", stream=True)
        t_00z = requests.get(f"{today_00z}{f_00z}", stream=True)

        y_18z = requests.get(f"{yday_18z}{f_18z}", stream=True)
        y_12z = requests.get(f"{yday_12z}{f_12z}", stream=True)
        y_06z = requests.get(f"{yday_06z}{f_06z}", stream=True)
        y_00z = requests.get(f"{yday_00z}{f_00z}", stream=True)    

    else:
        t_18z = requests.get(f"{today_18z}{f_18z}", stream=True, proxies=proxies)
        t_12z = requests.get(f"{today_12z}{f_12z}", stream=True, proxies=proxies)
        t_06z = requests.get(f"{today_06z}{f_06z}", stream=True, proxies=proxies)
        t_00z = requests.get(f"{today_00z}{f_00z}", stream=True, proxies=proxies)

        y_18z = requests.get(f"{yday_18z}{f_18z}", stream=True, proxies=proxies)
        y_12z = requests.get(f"{yday_12z}{f_12z}", stream=True, proxies=proxies)
        y_06z = requests.get(f"{yday_06z}{f_06z}", stream=True, proxies=proxies)
        y_00z = requests.get(f"{yday_00z}{f_00z}", stream=True, proxies=proxies)      

    if t_18z.status_code == 200:
        url = f"{today_18z}"
    elif t_18z.status_code != 200 and t_12z.status_code == 200:
        url = f"{today_12z}"
    elif t_12z.status_code != 200 and t_06z.status_code == 200:
        url = f"{today_06z}"
    elif t_06z.status_code != 200 and t_00z.status_code == 200:
        url = f"{today_00z}"
    elif t_00z.status_code != 200 and y_18z.status_code == 200:
        url = f"{yday_18z}"
    elif y_18z.status_code != 200 and y_12z.status_code == 200:
        url = f"{yday_12z}"
    elif y_12z.status_code != 200 and y_06z.status_code == 200:
        url = f"{yday_06z}"
    else:
        url = f"{yday_00z}"

    url_run = int(f"{url[aa]}{url[bb]}")
    
    print(url_run)
    
    print(url)
        
    return url, url_run           