# xmACIS2 Client

***def get_xmacis_data(station,
                    start_date=None,
                    end_date=None,
                    from_when=yesterday,
                    time_delta=30,
                    proxies=None,
                    clear_recycle_bin=True,
                    to_csv=False,
                    path='default',
                    filename='default',
                    notifications='on'):***

    This function is a client that downloads user-specified xmACIS2 data and returns a Pandas.DataFrame
    The user can also save the data as a CSV file in a specified location
    This client supports VPN/PROXY connections. 
    
    Required Arguments:
    
    1) station (String) - The 4 letter station ID (i.e. KRAL for Riverside Municipal Airport in Riverside, CA)
    
    Optional Arguments:
    
    1) start_date (String or Datetime) - Default=None. For users who want specific start and end dates for their analysis,
        they can either be passed in as a string in the format of 'YYYY-mm-dd' or as a datetime object.
        
    2) end_date (String or Datetime) - Default=None. For users who want specific start and end dates for their analysis,
        they can either be passed in as a string in the format of 'YYYY-mm-dd' or as a datetime object.
        
    3) from_when (String or Datetime) - Default=Yesterday. Default value is yesterday's date. 
       Dates can either be passed in as a string in the format of 'YYYY-mm-dd' or as a datetime object.
       
    4) time_delta (Integer) - Default=30. If from_when is NOT None, time_delta represents how many days IN THE PAST 
       from the time 'from_when.' (e.g. From January 31st back 30 days)
       
    5) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
                        
    6) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    7) to_csv (Boolean) - Default=False. When set to True, a CSV file of the data will be created and saved to the user specified or default path.
    
    8) path (String) - Default='default'. If set to 'default' the path will be "XMACIS2 DATA/file". Only change if you want to create your 
       directory path.
       
    9) filename (String) - Default='default'. If set to 'default' the filename will be the station ID. Only change if you want a custom
       filename. 
       
    10) notifications (String) - Default='on'. When set to 'on' a print statement to the user will tell the user their file saved to the path
        they specified. 
        
    Returns
    -------
    
    A Pandas.DataFrame of the xmACIS2 climate data the user specifies
