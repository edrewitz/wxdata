# Observed Atmospheric Soundings

***def get_observed_sounding_data(station_id, 
                               current=True, 
                               custom_time=None, 
                               comparison_24=False, 
                               proxies=None,
                               clear_recycle_bin=True):***

    This function scrapes the University of Wyoming Sounding Database and returns the data in a Pandas DataFrame

    Required Arguments:

    1) station_id (String or Integer) - User inputs the station_id as a string or an integer. 
    Some stations only have the ID by integer. Please see https://weather.uwyo.edu/upperair/sounding_legacy.html for more info. 
    
    Optional Arguments:

    1) current (Boolean) - Default = True. When set to True, the latest available data will be returned.
    If set to False, the user can download the data for a custom date/time of their choice. 

    2) custom_time (String) - If a user wants to download the data for a custom date/time, they must do the following:

        1. set current=False
        2. set custom_time='YYYY-mm-dd:HH'

    3) comparison_24 (Boolean) - Default = False. When set to True, the function will return the current dataset and dataset from 
       24-hours prior to the current dataset (i.e. 00z this evening vs. 00z yesterday evening). When set to False, only the 
       current dataset is returned. 

    4) proxies (String) - Default = None. If the user is requesting the data on a machine using a proxy server,
    the user must set proxy='proxy_url'. The default setting assumes the user is not using a proxy server conenction.
    
    5) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 

    Returns
    -------
    
    if comparison_24 == False: 
        A Pandas DataFrame of the University of Wyoming Sounding Data
    if comparison_24 == True:
        A Pandas DataFrame of the latest University of Wyoming Sounding Data
                                    AND
        A Pandas DataFrame of the University of Wyoming Sounding Data from 24-hours prior to the current DataFrame. 
