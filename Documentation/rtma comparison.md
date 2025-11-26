# Real-Time Mesoscale Analysis (RTMA) 24-Hour Comparison

***def rtma_comparison(model='rtma', 
         cat='analysis', 
         hours=24,
         proxies=None,
         process_data=True,
         clear_recycle_bin=True,
         western_bound=None,
         eastern_bound=None,
         southern_bound=None,
         northern_bound=None,
         clear_data=False,
         convert_temperature=True,
         convert_to='fahrenheit',
         custom_directory=None,
         chunk_size=8192,
         notifications='off'):***

    This function downloads the latest RTMA Dataset and the RTMA dataset from 24 hours prior to the current RTMA dataset and returns it as two xarray data arrays. 
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) model (String) - Default='rtma'. The RTMA model being used:
    
    RTMA Models
    -----------
    
    CONUS = 'rtma'
    Alaska = 'ak rtma'
    Hawaii = 'hi rtma'
    Puerto Rico = 'pr rtma'
    Guam = 'gu rtma'
    
    2) cat (String) - Default='analysis'. The category of the RTMA dataset. 
    
    RTMA Categories
    ---------------
    
    analysis - Latest RTMA Analysis
    error - Latest RTMA Error
    surface 1 hour forecast - RTMA Surface 1 Hour Forecast
    
    3) hours (Integer) - Default=24. The amount of hours previous to the current dataset for the comparison dataset. 
    
    4) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                        }
                        
    5) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    6) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    7) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    8) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    9) southern_bound (Float or Integer) - Default=-90. The northern bound of the data needed.

    10) northern_bound (Float or Integer) - Default=90. The southern bound of the data needed.
    
    11) clear_data (Boolean) - Default=False. When set to True, the current data in the folder is deleted
        and new data is downloaded automatically with each run. 
        This setting is recommended for users who wish to use a medley of different comparisons. 
        
    12) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    13) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    14) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
        
    15) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    16) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    Returns
    -------
    
    1) ds - The current RTMA dataset
    
    2) ds_dt - The RTMA comparison dataset from a user specified amount of hours prior to the current dataset. 
    
    All with variable keys converted from the GRIB format to a Plain Language format. 
    
    Variable Keys
    -------------
    
    'orography'
    'surface_pressure'
    '2m_temperature'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_specific_humidity'
    'surface_visibility'
    'cloud_ceiling_height'
    'total_cloud_cover'
    '10m_u_wind_component'
    '10m_v_wind_component'
    '10m_wind_direction'
    '10m_wind_speed'
    '10m_wind_gust'
    '2m_apparent_temperature'
    '2m_dew_point_depression'
