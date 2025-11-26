# FEMS: Get NFDRS Forecast Data For A RAWS SIG For A Geographic Area Coordination Center Region

***def get_nfdrs_forecast_data(gacc_region, 
                            fuel_model='Y',
                            proxies=None,
                            clear_recycle_bin=True):***

    This function retrieves the latest fuels forecast data from FEMS.

    Required Arguments:

    1) gacc_region (String) - The 4-letter GACC abbreviation
    
    Optional Arguments:

    1) fuel_model (String) - Default='Y'. The fuel model being used. 
        Fuel Models List:

        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash 
        
    2) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    3) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }

    Returns
    -------
    
    A list of NFDRS forecast data in the form of a Pandas DataFrames listed by each Predictive Services Area
