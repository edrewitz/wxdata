# FEMS: Get Single RAWS Station Data

***def get_single_station_data(station_id, 
                            number_of_days, 
                            start_date=None, 
                            end_date=None, 
                            fuel_model='Y', 
                            to_csv=True,
                            clear_recycle_bin=True):***

This function retrieves the dataframe for a single RAWS station in FEMS

Required Arguments:

1) station_id (Integer) - The WIMS or RAWS ID of the station. 

2) number_of_days (Integer or String) - How many days the user wants the summary for (90 for 90 days).
If the user wants to use a custom date range enter 'Custom' or 'custom' in this field. 

Optional Arguments:

1) start_date (String) - Default = None. The start date if the user wants to define a custom period. Enter as a string
in the following format 'YYYY-mm-dd'

2) end_date (String) - Default = None. The end date if the user wants to define a custom period. Enter as a string
in the following format 'YYYY-mm-dd'

3) fuel_model (String) - Default = 'Y'. The fuel model being used. 

        Fuel Models List:
        
        Y - Timber
        X - Brush
        W - Grass/Shrub
        V - Grass
        Z - Slash

4) to_csv (Boolean) - Default = True. This will save the data into a CSV file and build a directory to hold the CSV files. 

5) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
of the program you are calling WxData. This setting is to help preserve memory on the machine. 

Returns
-------

A Pandas DataFrame of the NFDRS data from FEMS.   
