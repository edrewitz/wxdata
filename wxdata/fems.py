import os
import pandas as pd
import raws_sigs as raws

try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta

def get_single_station_data(station_id, number_of_days, start_date=None, end_date=None, fuel_model='Y', to_csv=True):

    """
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

    Returns: A Pandas DataFrame of the NFDRS data from FEMS.            

    """

    if number_of_days == 'Custom' or number_of_days == 'custom':

        df = pd.read_csv(f"https://fems.fs2c.usda.gov/api/climatology/download-nfdr?stationIds={str(station_id)}&endDate={end_date}Z&startDate={start_date}Z&dataFormat=csv&dataset=all&fuelModels={fuel_model}")    
    else:

        try:
            now = datetime.now(UTC)
        except Exception as e:
            now = datetime.utcnow()
            
        start = now - timedelta(days=number_of_days)
        
        df = pd.read_csv(f"https://fems.fs2c.usda.gov/api/climatology/download-nfdr?stationIds={str(station_id)}&endDate={now.strftime(f'%Y-%m-%d')}T{now.strftime(f'%H:%M:%S')}Z&startDate={start.strftime(f'%Y-%m-%d')}T{start.strftime(f'%H:%M:%S')}Z&dataFormat=csv&dataset=all&fuelModels={fuel_model}") 

    if to_csv == True:

        if os.path.exists(f"FEMS Data"):
            pass
        else:
            os.mkdir(f"FEMS Data")

        fname = f"{station_id} {number_of_days} Days Fuel Model {fuel_model}.csv"
        
        try:
            os.remove(f"FEMS Data/{fname}")
        except Exception as e:
            pass

        file = df.to_csv(fname, index=False)
        os.replace(f"{fname}", f"FEMS Data/{fname}")
    else:
        pass
    
    return df


def get_raws_sig_data(gacc_region, number_of_years_for_averages, fuel_model, start_date):

    """
    This function does the following:

    1) Downloads all the data for the Critical RAWS Stations for each GACC Region

    2) Builds the directory where the RAWS data CSV files will be hosted

    3) Saves the CSV files to the paths which are sorted by Predictive Services Area (PSA)

    Required Arguments:

    1) gacc_region (String) - The 4-letter GACC abbreviation

    2) number_of_years_for_averages (Integer) - Default = 10. The number of years for the average values to be calculated on. 

    3) fuel_model (String) - Default = 'Y'. The fuel model being used. 
       Fuel Models List:

       Y - Timber
       X - Brush
       W - Grass/Shrub
       V - Grass
       Z - Slash 

    4) start_date (String) - Default = None. If the user wishes to use a selected start date as the starting point enter the start_date
       as a string in the following format: YYYY-mm-dd

    Returns: The RAWS CSV data files sorted into the folders which are the different SIGs for each GACC
    """

    gacc_region = gacc_region.upper()

    df_station_list = raws.get_sigs(gacc_region)

    try:
        now = datetime.now(UTC)
    except Exception as e:
        now = datetime.utcnow()

    if start_date == None:
        number_of_days = number_of_years_for_averages * 365
            
        start = now - timedelta(days=number_of_days)

    else:
        start_date = start_date
        
        year = f"{start_date[0]}{start_date[1]}{start_date[2]}{start_date[3]}"
        month = f"{start_date[5]}{start_date[6]}"
        day = f"{start_date[8]}{start_date[9]}"

        year = int(year)
        month = int(month)
        day = int(day)

        start = datetime(year, month, day, 0, 0, 0)

    for station, psa in zip(df_station_list['RAWSID'], df_station_list['PSA Code']):
        
        df = pd.read_csv(f"https://fems.fs2c.usda.gov/api/climatology/download-nfdr?stationIds={station}&endDate={now.strftime('%Y-%m-%dT%H:%M:%S')}Z&startDate={start.strftime('%Y-%m-%dT%H:%M:%S')}Z&dataFormat=csv&dataset=observation&fuelModels={fuel_model}")
            
        if os.path.exists(f"FEMS Data"):
            pass
        else:
            os.mkdir(f"FEMS Data")   

        if os.path.exists(f"FEMS Data/Stations"):
            pass
        else:
            os.mkdir(f"FEMS Data/Stations") 

        if os.path.exists(f"FEMS Data/Stations/{gacc_region}"):
            pass
        else:
            os.mkdir(f"FEMS Data/Stations/{gacc_region}") 

        if os.path.exists(f"FEMS Data/Stations/{gacc_region}/{psa}"):
            pass
        else:
            os.mkdir(f"FEMS Data/Stations/{gacc_region}/{psa}") 

        fname = f"{station}.csv"

        file = df.to_csv(fname, index=False)
        os.replace(f"{fname}", f"FEMS Data/Stations/{gacc_region}/{psa}/{fname}")


def get_nfdrs_forecast_data(gacc_region, fuel_model):

    gacc_region = gacc_region.upper()
    
    df_station_list = raws.get_sigs(gacc_region)
    
    try:
        start = datetime.now(UTC)
    except Exception as e:
        start = datetime.utcnow()

    end = start + timedelta(days=7)

    for station, psa in zip(df_station_list['RAWSID'], df_station_list['PSA Code']):
        df = pd.read_csv(f"https://fems.fs2c.usda.gov/api/climatology/download-nfdr-daily-summary/?dataset=forecast&startDate={start.strftime('%Y-%m-%d')}&endDate={end.strftime('%Y-%m-%d')}&dataFormat=csv&stationIds={station}&fuelModels={fuel_model}")

        if os.path.exists(f"FEMS Data"):
            pass
        else:
            os.mkdir(f"FEMS Data")   

        if os.path.exists(f"FEMS Data/Forecasts"):
            pass
        else:
            os.mkdir(f"FEMS Data/Forecasts") 

        if os.path.exists(f"FEMS Data/Forecasts/{gacc_region}"):
            pass
        else:
            os.mkdir(f"FEMS Data/Forecasts/{gacc_region}") 

        if os.path.exists(f"FEMS Data/Forecasts/{gacc_region}/{psa}"):
            pass
        else:
            os.mkdir(f"FEMS Data/Forecasts/{gacc_region}/{psa}") 

        fname = f"{station}.csv"

        file = df.to_csv(fname, index=False)
        os.replace(f"{fname}", f"FEMS Data/Forecasts/{gacc_region}/{psa}/{fname}")