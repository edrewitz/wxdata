# Global Ensemble Forecast System 0.50 X 0.50 DEGREE (GEFS0P50)

***def gefs0p50(cat='mean', 
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
                        'water equivalent of accumulated snow depth']):***

This function downloads the latest GEFS0P50 data for a region specified by the user

Required Arguments: None

Optional Arguments:

1) cat (string) - Default='mean'. The category of the ensemble data. 

Valid categories:
      1) 'mean'
      2) 'members'
      3) 'spread'

2) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GEFS0P50
goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
384 by the nereast increment of 3 hours. 

3) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

4) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

5) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

6) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

 proxies=None ---> proxies={
                     'http':'http://url',
                     'https':'https://url'
                  }

8) members (List) - Default=All 30 ensemble members. The individual ensemble members. There are 30 members in this ensemble.  

9) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
 data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
 
10) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
  of the program you are calling WxData. This setting is to help preserve memory on the machine. 
  
11) variables (List) - A list of variable names the user wants to download in plain language. 
    
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

