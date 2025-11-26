# FEMS: Get NFDRS Forecast Data For A RAWS SIG For A Geographic Area Coordination Center Region

***def get_raws_sig_data(gacc_region, 
                      number_of_years_for_averages=15, 
                      fuel_model='Y',
                      proxies=None, 
                      start_date=None,
                      clear_recycle_bin=True):***

    This function does the following:

    1) Downloads all the data for the Critical RAWS Stations for each GACC Region

    2) Builds the directory where the RAWS data CSV files will be hosted

    3) Saves the CSV files to the paths which are sorted by Predictive Services Area (PSA)

    Required Arguments:

    1) gacc_region (String) - The 4-letter GACC abbreviation
    
    Optional Arguments:

    1) number_of_years_for_averages (Integer) - Default=15. The number of years for the average values to be calculated on. 

    2) fuel_model (String) - Default='Y'. The fuel model being used. 
        Fuel Models List:

        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash 

    3) start_date (String) - Default=None. If the user wishes to use a selected start date as the starting point enter the start_date
        as a string in the following format: YYYY-mm-dd
        
    4) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    5) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }

    Returns
    ------- 
    
        A list of Pandas DataFrames 
        ---------------------------
        
        1) Raw Data for each PSA
        2) Average for each PSA
        3) Minimum for each PSA
        4) Maximum for each PSA
        5) Dates
