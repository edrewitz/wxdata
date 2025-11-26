import pandas as pd
import os
import shutil
import wxdata.fems.raws_sigs as raws
import wxdata.client.client as client

from wxdata.utils.recycle_bin import *
from calendar import isleap

try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta 
    
try:
    utc_time = datetime.now(UTC)
except Exception as e:
    utc_time = datetime.utcnow()
    
    
def get_psa_ids(gacc_region):
    
    """
    This function returns the Predictive Services Areas IDs for each GACC. 
    
    Required Arguments:
    
    1) gacc_region (String) - The 4-letter GACC abbreviation
    
    GACC Abbreviations
    ------------------
    
    oscc - South Ops
    oncc - North Ops
    nwcc - Northwest Coordination Center
    swcc - Southwest Coordination Center
    nrcc - Northern Rockies Coordination Center
    gbcc - Great Basin Coordination Center
    aicc - Alaska Interagency Coordination Center
    rmcc - Rocky Mountain Coordination Center
    sacc - Southern Area Coordination Center
    eacc - Eastern Area Coordination Center
    
    Returns
    -------
    
    The PSA IDs for a GACC. 
    """

    gacc_region = gacc_region.upper()

    if gacc_region == "SACC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16",
                  "17A",
                  "17B",
                  "18",
                  "19",
                  "20",
                  "21A",
                  "21B",
                  "21C",
                  "22A",
                  "22B",
                  "23",
                  "24",
                  "25",
                  "25B",
                  "26",
                  "27",
                  "28A",
                  "28B",
                  "29",
                  "30",
                  "31A",
                  "31B",
                  "31C",
                  "32",
                  "33",
                  "34",
                  "35",
                  "36",
                  "37",
                  "38",
                  "39",
                  "40",
                  "41",
                  "42",
                  "46",
                  "47",
                  "48",
                  "49",
                  "50",
                  "52"
                 ]

    if gacc_region == 'ONCC':
        psaIDs = ["1",
                  "2",
                  "3A",
                  "3B",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8"
                 ]

    if gacc_region == "OSCC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16"
                 ]

    if gacc_region == "GBCC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16",
                  "17",
                  "18",
                  "19",
                  "20",
                  "21",
                  "22",
                  "23",
                  "24",
                  "25",
                  "26",
                  "27",
                  "28",
                  "29",
                  "30",
                  "31",
                  "32",
                  "33",
                  "34",
                  "35"                  
                 ]

    if gacc_region == "EACC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16",
                  "17",
                  "18",
                  "19",
                  "20",
                  "21",
                  "22",
                  "23",
                  "24"
                 ]


    if gacc_region == "NRCC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16",
                  "17",
                  "18"
                 ]

    if gacc_region == "NWCC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12"
                 ]

    if gacc_region == "RMCC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16",
                  "17",
                  "18",
                  "19",
                  "20",
                  "21",
                  "22",
                  "23",
                  "24",
                  "25",
                  "26",
                  "27",
                  "28"
                 ]

    if gacc_region == "SWCC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6N",
                  "6S",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14N"
                 ]
                  
    return psaIDs                 

def get_single_station_data(station_id, 
                            number_of_days, 
                            start_date=None, 
                            end_date=None, 
                            fuel_model='Y', 
                            clear_recycle_bin=True,
                            path='FEMS Data',
                            proxies=None):

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
    
    5) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    6) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        }

    7) path (String) - Default='FEMS Data". The parent directory to the FEMS data files.
    
    Returns
    -------
    
    A Pandas DataFrame of the NFDRS data from FEMS.            

    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    fuel_model = fuel_model.upper()
    
    fname = f"{station_id} {number_of_days} Days Fuel Model {fuel_model}.csv"

    if number_of_days == 'Custom' or number_of_days == 'custom':

        df = client.get_csv_data(f"https://fems.fs2c.usda.gov/api/climatology/download-nfdr?"
                            f"stationIds={str(station_id)}&endDate={end_date}Z&startDate={start_date}Z&"
                            f"dataFormat=csv&dataset=all&fuelModels={fuel_model}",
                            path,
                            fname,
                            proxies=proxies,
                            notifications='off',
                            clear_data=False)
            
    else:

        try:
            now = datetime.now(UTC)
        except Exception as e:
            now = datetime.utcnow()
            
        start = now - timedelta(days=number_of_days)

        df = client.get_csv_data(f"https://fems.fs2c.usda.gov/api/climatology/download-nfdr?"
                                 f"stationIds={str(station_id)}&endDate={now.strftime(f'%Y-%m-%d')}T{now.strftime(f'%H:%M:%S')}Z&"
                                 f"startDate={start.strftime(f'%Y-%m-%d')}T{start.strftime(f'%H:%M:%S')}Z&"
                                 f"dataFormat=csv&dataset=all&fuelModels={fuel_model}",
                                path,
                                fname,
                                proxies=proxies,
                                notifications='off',
                                clear_data=False)
    
    return df


def get_raws_sig_data(gacc_region, 
                      number_of_years_for_averages=15, 
                      fuel_model='Y',
                      proxies=None, 
                      start_date=None,
                      clear_recycle_bin=True):

    """
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
    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass

    gacc_region = gacc_region.upper()
    fuel_model = fuel_model.upper()

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
        
        fname = f"{station}.csv"
         
        client.get_csv_data(f"https://fems.fs2c.usda.gov/api/climatology/download-nfdr?"
                                 f"stationIds={station}&endDate={now.strftime('%Y-%m-%dT%H:%M:%S')}Z&"
                                 f"startDate={start.strftime('%Y-%m-%dT%H:%M:%S')}Z&"
                                 f"dataFormat=csv&dataset=observation&fuelModels={fuel_model}",
                                    f"FEMS Data/Stations/{gacc_region}/{psa}",
                                    fname,
                                    proxies=proxies,
                                    notifications='off',
                                    return_pandas_df=False)    
        
    raws.get_psa_percentiles(gacc_region)
    raws.station_stats(gacc_region)
    raws.get_stats(gacc_region)
    raws.get_psa_climatology(gacc_region)
    raws.sort_data_by_psa(gacc_region)

    data_dir = f"FEMS Data/{gacc_region}/PSA Data"
    percentiles_dir = f"FEMS Data/{gacc_region}/PSA Percentiles"
    climo_avg_dir = f"FEMS Data/{gacc_region}/PSA Climo/AVG"
    climo_min_dir = f"FEMS Data/{gacc_region}/PSA Climo/MIN"
    climo_max_dir = f"FEMS Data/{gacc_region}/PSA Climo/MAX"

    percentiles = pd.read_csv(f"FEMS Data/{gacc_region}/PSA Percentiles/PSA_Percentiles.csv")

    leap = isleap(utc_time.year)
    if start_date == None:
        if leap == False:
            days = number_of_years_for_averages * 365
        else:
            days = number_of_years_for_averages * 366
        start_date = utc_time - timedelta(days=days)
        start_year = start_date.year
        xmin = start_date
        xmax = utc_time

    else:
        start_date = start_date
        start_year = f"{start_date[0]}{start_date[1]}{start_date[2]}{start_date[3]}"
        start_month = f"{start_date[5]}{start_date[6]}"
        start_day = f"{start_date[8]}{start_date[9]}"
        xmin = datetime(int(start_year), int(start_month), int(start_day))
        xmax = utc_time
    
    psa = 1

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    files = os.listdir(f"{data_dir}")
    psa = 1

    psa_IDs = get_psa_ids(gacc_region)              
            
    data = []
    climo_avg = []
    climo_max = []
    climo_min = []       
    for i in range(0, len(files)):

        fname = f"{psa_IDs[i]}.png"
        psaID = psa_IDs[i]

        try:
            df_data = pd.read_csv(f"{data_dir}/zone_{psa}.csv") 
            df_climo_avg = pd.read_csv(f"{climo_avg_dir}/zone_{psa}.csv") 
            df_climo_min = pd.read_csv(f"{climo_min_dir}/zone_{psa}.csv") 
            df_climo_max = pd.read_csv(f"{climo_max_dir}/zone_{psa}.csv") 
            
            data.append(df_data)
            climo_avg.append(df_climo_avg)
            climo_min.append(df_climo_min)
            climo_max.append(df_climo_max)
        except Exception as e:
            pass

        try:
            dates = pd.to_datetime(df_data['dates'])
        except Exception as e:
            pass
            
    return data, climo_avg, climo_min, climo_max, dates


def get_nfdrs_forecast_data(gacc_region, 
                            fuel_model='Y',
                            proxies=None,
                            clear_recycle_bin=True):

    """
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
    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass

    gacc_region = gacc_region.upper()
    fuel_model = fuel_model.upper()
    
    df_station_list = raws.get_sigs(gacc_region)
    
    try:
        start = datetime.now(UTC)
    except Exception as e:
        start = datetime.utcnow()

    end = start + timedelta(days=7)

    psas = []
    for station, psa in zip(df_station_list['RAWSID'], df_station_list['PSA Code']):

        fname = f"{station}.csv"
        client.get_csv_data(f"https://fems.fs2c.usda.gov/api/climatology/download-nfdr-daily-summary/?"
                            f"dataset=forecast&startDate={start.strftime('%Y-%m-%d')}&endDate={end.strftime('%Y-%m-%d')}&"
                            f"dataFormat=csv&stationIds={station}&fuelModels={fuel_model}",
                                    f"FEMS Data/Forecasts/{gacc_region}/{psa}",
                                    fname,
                                    proxies=proxies,
                                    notifications='off',
                                    return_pandas_df=False) 

        psas.append(psa)
        
    raws.station_forecast(gacc_region)
    raws.sort_forecasts_by_psa(gacc_region)
    
    forecast_dir = f"FEMS Data/{gacc_region}/PSA Forecast"
    
    dfs = []
    for p in range(0, len(psas)):
        try:
            df = pd.read_csv(f"{forecast_dir}/zone_{p}.csv") 
            dfs.append(df)
        except Exception as e:
            pass
    
    return dfs