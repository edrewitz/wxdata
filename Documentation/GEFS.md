**Global Ensemble Forecast System (GEFS)**

###### Table of Contents

1. [GEFS0P50]()
2. [GEFS0P50 SECONDARY PARAMETERS]()
3. [GEFS0P25]()

###### GEFS0P50

This function retrives the latest GEFS0P50 data. If the data is not previously downloaded nor up to date, the function
will download and pre-process the latest dataset. 

To avoid bans from the data servers, the function will scan the data server and locally hosted files and if the 
files are up to date, the function will skip downloading the newest dataset. 

Required Arguments:

1) cat (String) - The category of the data. (i.e. mean, control, all members)

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

