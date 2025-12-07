import requests
import time
import sys
import os
import json
import urllib
import numpy as np
import pandas as pd

from io import BytesIO
from datetime import datetime, timedelta
from wxdata.utils.xmacis2_cleanup import clean_pandas_dataframe
from wxdata.utils.recycle_bin import *

# Getting yesterday's date for the default end date for the xmACIS2 client

now = datetime.now()
yesterday = now - timedelta(days=1)

year = yesterday.year
month = yesterday.month
day = yesterday.day

if day >= 10:
    yesterday = f"{year}-{month}-{day}"
else:
    yesterday = f"{year}-{month}-0{day}"

def get_gridded_data(url,
             path,
             filename,
             proxies=None,
             chunk_size=8192,
             notifications='on',
             clear_recycle_bin=True):
    
    """
    This function is the client that retrieves gridded weather/climate data (GRIB2 and NETCDF) files. 
    This client supports VPN/PROXY connections. 
    
    Required Arguments:
    
    1) url (String) - The download URL to the file. 
    
    2) path (String) - The directory where the file is saved to. 
    
    3) filename (String) - The name the user wishes to save the file as. 
    
    Optional Arguments:
    
    1) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
                        
    2) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    3) notifications (String) - Default='on'. Notification when a file is downloaded and saved to {path}
    
    4) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
    
    Returns
    -------
    
    Gridded weather/climate data files (GRIB2 or NETCDF) saved to {path}    
    """
    
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    try:
        os.makedirs(f"{path}")
    except Exception as e:
        pass

    if proxies == None:
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status() 
                with open(f"{path}/{filename}", 'wb') as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
            if notifications == 'on':
                print(f"Successfully saved {filename} to f:{path}")
            else:
                pass
        except requests.exceptions.RequestException as e:
            for i in range(0, 6, 1):
                if i < 3:
                    print(f"Alert: Network connection unstable.\nWaiting 30 seconds then automatically trying again.\nAttempts remaining: {5 - i}")
                    time.sleep(30)
                else:
                    print(f"Alert: Network connection unstable.\nWaiting 60 seconds then automatically trying again.\nAttempts remaining: {5 - i}")
                    time.sleep(60)  
                    
                try:
                    with requests.get(url, stream=True) as r:
                        r.raise_for_status() 
                        with open(f"{path}/{filename}", 'wb') as f:
                            for chunk in r.iter_content(chunk_size=chunk_size):
                                f.write(chunk)
                    if notifications == 'on':
                        print(f"Successfully saved {filename} to f:{path}")  
                    break
                except requests.exceptions.RequestException as e:
                    i = i 
                    if i >= 5:
                        print(f"Error - File Cannot Be Downloaded.\nError Code: {e}")    
                        sys.exit(1)      
                        
        finally:
            if r:
                r.close() # Ensure the connection is closed.
            
    else:
        try:
            with requests.get(url, stream=True, proxies=proxies) as r:
                r.raise_for_status() 
                with open(f"{path}/{filename}", 'wb') as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
            if notifications == 'on':
                print(f"Successfully saved {filename} to f:{path}")
            else:
                pass
        except requests.exceptions.RequestException as e:
            for i in range(0, 6, 1):
                if i < 3:
                    print(f"Alert: Network connection unstable.\nWaiting 30 seconds then automatically trying again.\nAttempts remaining: {5 - i}")
                    time.sleep(30)
                else:
                    print(f"Alert: Network connection unstable.\nWaiting 60 seconds then automatically trying again.\nAttempts remaining: {5 - i}")
                    time.sleep(60)  
                    
                try:
                    with requests.get(url, stream=True, proxies=proxies) as r:
                        r.raise_for_status() 
                        with open(f"{path}/{filename}", 'wb') as f:
                            for chunk in r.iter_content(chunk_size=chunk_size):
                                f.write(chunk)
                    if notifications == 'on':
                        print(f"Successfully saved {filename} to f:{path}")  
                    break
                except requests.exceptions.RequestException as e:
                    i = i 
                    if i >= 5:
                        print(f"Error - File Cannot Be Downloaded.\nError Code: {e}")    
                        sys.exit(1)    
                        
        finally:
            if r:
                r.close() # Ensure the connection is closed.
                        
                        
def get_csv_data(url,
                 path,
                 filename,
                 proxies=None,
                 notifications='on',
                 return_pandas_df=True,
                 clear_recycle_bin=True):
    
    """
    This function is the client that retrieves CSV files from the web.
    This client supports VPN/PROXY connections. 
    User also has the ability to read the CSV file and return a Pandas.DataFrame()
    
    Required Arguments:
    
    1) url (String) - The download URL to the file. 
    
    2) path (String) - The directory where the file is saved to. 
    
    3) filename (String) - The name the user wishes to save the file as. 
    
    Optional Arguments:
    
    1) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
    
    2) notifications (String) - Default='on'. Notification when a file is downloaded and saved to {path}
    
    3) return_pandas_df (Boolean) - Default=True. When set to True, a Pandas.DataFrame() of the data inside the CSV file will be returned to the user. 
    
    4) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
    
    
    Returns
    -------
    
    A CSV file saved to {path}
    
    if return_pandas_df=True - A Pandas.DataFrame()
    """
    
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    try:
        os.makedirs(f"{path}")
    except Exception as e:
        pass
    
    if proxies==None:
        try:
            response = requests.get(url)
        except Exception as e:
            for i in range(0, 6, 1):
                if i < 3:
                    print(f"Alert: Network connection unstable.\nWaiting 30 seconds then automatically trying again.\nAttempts remaining: {5 - i}")
                    time.sleep(30)
                else:
                    print(f"Alert: Network connection unstable.\nWaiting 60 seconds then automatically trying again.\nAttempts remaining: {5 - i}")
                    time.sleep(60)  
                    
                try:
                    response = requests.get(url)
                    break
                except Exception as e:
                    i = i                    
                    if i >= 5:
                        print(f"Error - File Cannot Be Downloaded.\nError Code: {e}")    
                        sys.exit(1)    
        finally:
            if response:
                response.close() # Ensure the connection is closed.
                        
    else:
        try:
            response = requests.get(url, proxies=proxies)
        except Exception as e:
            for i in range(0, 6, 1):
                if i < 3:
                    print(f"Alert: Network connection unstable.\nWaiting 30 seconds then automatically trying again.\nAttempts remaining: {5 - i}")
                    time.sleep(30)
                else:
                    print(f"Alert: Network connection unstable.\nWaiting 60 seconds then automatically trying again.\nAttempts remaining: {5 - i}")
                    time.sleep(60)  
                    
                try:
                    response = requests.get(url, proxies=proxies)
                    break
                except Exception as e:
                    i = i                    
                    if i >= 5:
                        print(f"Error - File Cannot Be Downloaded.\nError Code: {e}")    
                        sys.exit(1) 

                
                   
    data_stream = BytesIO(response.content)
    if response:
        response.close() # Ensure the connection is closed.
    
    df = pd.read_csv(data_stream)
    
    df.to_csv(f"{path}/{filename}", index=False)
    if notifications == True:
        print(f"{filename} saved to {path}")
    else:
        pass
    
    if return_pandas_df == True:
    
        return df
    
    else:
        pass
    
    
def get_xmacis_data(station,
                    start_date=None,
                    end_date=None,
                    from_when=yesterday,
                    time_delta=30,
                    proxies=None,
                    clear_recycle_bin=True,
                    to_csv=False,
                    path='default',
                    filename='default',
                    notifications='on'):
    
    """
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
    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass  
    
    station = station.upper()
    
    if path == 'default':
        path = f"XMACIS2 DATA"
        if filename == 'default':
            full_path = f"XMACIS2 DATA/{station}.csv"
        else:
            full_path = f"XMACIS2 DATA/{filename}.csv"
    else:
        if filename == 'default':
            full_path = f"{path}/{station}.csv"
        else:
            full_path = f"{path}/{filename}.csv"
    
    if start_date == None and end_date == None:
        try:
            if time_delta != None and from_when != None:
                if type(from_when) == type('String'):
                    iyear = int(f"{from_when[0]}{from_when[1]}{from_when[2]}{from_when[3]}")
                    imonth = int(f"{from_when[5]}{from_when[6]}")
                    iday = int(f"{from_when[8]}{from_when[9]}")
                    end_date = datetime(iyear, imonth, iday)
                else:
                    end_date = from_when
                    
                start_date = end_date - timedelta(days=time_delta)  
                    
        except Exception as e:
            print(f"""Error: Invalid Time Entry
                
                    The user must have one of the following for a valid time entry:
                    
                    time_delta = days (Integer) - How many days back?
                    
                    from_when = date (String) format (YYYY-mm-dd) 

                        The result will be "How many days back from when?"
                        
                                        OR
                                        
                        time_delta=None
                        
                        from_when=None
                        
                        In this case enter the start_date and end_date as strings in the YYYY-mm-dd format
                
                """)   
    else:
        start_date = start_date
        end_date = end_date
    
    if type(start_date) != type('String'):
        syear = str(start_date.year)
        smonth = str(start_date.month)
        sday = str(start_date.day)
        start_date = f"{syear}-{smonth}-{sday}"
    else:
        pass
    if type(end_date) != type('String'):
        eyear = str(end_date.year)
        emonth = str(end_date.month)
        eday = str(end_date.day)
        end_date = f"{eyear}-{emonth}-{eday}"
    else:
        pass
    

    input_dict = {
        'sid': station,
        'sdate': start_date,
        'edate': end_date,
        'elems': ["maxt","mint","avgt",{"name":"avgt","normal":"departure"},"hdd","cdd","pcpn","snow","snwd", "gdd"],
        'output': 'json'
    }


    output_cols = ['Date', 'Maximum Temperature', 'Minimum Temperature', 'Average Temperature', 'Average Temperature Departure', 'Heating Degree Days', 'Cooling Degree Days', 'Precipitation', 'Snowfall', 'Snow Depth', 'Growing Degree Days']
        
    if proxies == None:
        response = requests.post('http://data.rcc-acis.org/StnData', 
                                 json=input_dict)
    else:
        response = requests.post('http://data.rcc-acis.org/StnData', 
                                 json=input_dict,
                                 proxies=proxies)
        
    response.close()
        
    data = response.json()
    
    df = pd.json_normalize(data,
                      record_path=['data'])
    
    df.columns = output_cols
    
    df = clean_pandas_dataframe(df)
    
    if to_csv == True:
        try:
            os.makedirs(path)
        except Exception as e:
            pass
        df.to_csv(f"{full_path}", index=False)
        if notifications == 'on':
            print(f"{station} Data Saved: {full_path}")
    else:
        pass
    
    return df
    
    
    
        