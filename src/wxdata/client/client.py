import requests
import time
import sys
import os
import pandas as pd

from io import BytesIO
from wxdata.utils.recycle_bin import *

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