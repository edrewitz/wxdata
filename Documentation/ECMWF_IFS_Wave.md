# ECMWF IFS Wave

***def ecmwf_ifs_wave(final_forecast_hour=144,
              western_bound=-180,
              eastern_bound=180,
              northern_bound=90,
              southern_bound=-90,
              step=3,
              proxies=None,
              process_data=True,
              clear_recycle_bin=True,
              custom_directory=None,
              chunk_size=8192,
              notifications='off'):***

    This function scans for the latest ECMWF IFS Wave dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 360. The final forecast hour the user wishes to download. The ECMWF IFS Wave
    goes out to 144 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    144 by the nereast increment of 3 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    10) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
        
    11) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    12) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
        
    Returns
    -------
    
    An xarray data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF IFS Wave Variable Keys (After Post-Processing)
    -------------------------------------------------------------------
    
    'mean_zero_crossing_wave_period'
    'significant_height_of_combined_waves_and_swell'
    'mean_wave_direction'
    'peak_wave_period'
    'mean_wave_period'
