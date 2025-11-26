# Real-Time Mesoscale Analysis (RTMA)

***def rtma(model='rtma', 
         cat='analysis', 
         proxies=None,
         process_data=True,
         clear_recycle_bin=True,
         western_bound=None,
         eastern_bound=None,
         southern_bound=None,
         northern_bound=None,
         convert_temperature=True,
         convert_to='fahrenheit',
         custom_directory=None,
         clear_data=False,
         chunk_size=8192,
         notifications='off'):***


    This function downloads the latest RTMA Dataset and returns it as an xarray data array. 
    
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
    
    3) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                        }
                        
    4) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    5) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    6) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    7) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    8) southern_bound (Float or Integer) - Default=-90. The northern bound of the data needed.

    9) northern_bound (Float or Integer) - Default=90. The southern bound of the data needed.
    
    10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    12) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
        
    13) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    14) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    Returns
    -------
    
    An xarray data array of the RTMA Dataset with variable keys converted from the GRIB format to a Plain Language format. 
    
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
