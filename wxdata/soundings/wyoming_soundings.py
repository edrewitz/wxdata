"""
This file hosts the function to retrieve Wyoming Sounding Data.

This data is for observed soundings. 

(C) Eric J. Drewitz
"""
# Imports the needed libraries
import requests
import pandas as pd
import metpy.calc as mpcalc
import sys
import pyximport
pyximport.install()

from ..soundings.calc import(
    get_u_and_v,
    relative_humidity,
    saturation_vapor_pressure
)
from metpy.units import units
from bs4 import BeautifulSoup
from io import StringIO

try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta

try:
    now = datetime.now(UTC)
except Exception as e:
    now = datetime.utcnow()


def station_ids(station_id):

    """
    This function returns the station number for a station ID

    Required Arguments:

    1) station_id (String)

    Returns
    -------

    An integer for the station number
    """

    station_id = station_id.upper()

    station_ids = {

        'NKX':'72293',
        'VBG':'72393'

    }

    station_number = station_ids.get(station_id)

    return station_number
    

def get_observed_sounding_data(station_id, current=True, custom_time=None, comparison_24=False, proxies=None):

    """
    This function scrapes the University of Wyoming Sounding Database and returns the data in a Pandas DataFrame

    Required Arguments:

    1) station_id (String or Integer) - User inputs the station_id as a string or an integer. 
    Some stations only have the ID by integer. Please see http://www.weather.uwyo.edu/upperair/naconf.html for more info. 

    2) current (Boolean) - Default = True. When set to True, the latest available data will be returned.
    If set to False, the user can download the data for a custom date/time of their choice. 

    3) custom_time (String) - If a user wants to download the data for a custom date/time, they must do the following:

        1. set current=False
        2. set custom_time='YYYY-mm-dd:HH'

    4) comparison_24 (Boolean) - Default = False. When set to True, the function will return the current dataset and dataset from 
       24-hours prior to the current dataset (i.e. 00z this evening vs. 00z yesterday evening). When set to False, only the 
       current dataset is returned. 

    5) proxies (String) - Default = None. If the user is requesting the data on a machine using a proxy server,
    the user must set proxy='proxy_url'. The default setting assumes the user is not using a proxy server conenction.

    Returns
    -------
    
    if comparison_24 == False: 
        A Pandas DataFrame of the University of Wyoming Sounding Data
    if comparison_24 == True:
        A Pandas DataFrame of the latest University of Wyoming Sounding Data
                                    AND
        A Pandas DataFrame of the University of Wyoming Sounding Data from 24-hours prior to the current DataFrame. 
    """

    if type(station_id) == type(0):
        station_number = station_id
    else:
        station_number = station_ids(station_id)

    if comparison_24 == False:

        if current == True:
            date = now
            if date.hour <= 12:
                hour = 00
            else:
                hour = 12
    
            y = date.year
            m = date.month
            d = date.day
            new_date = datetime(y, m, d, hour)
        else:
            year = int(f"{custom_time[0]}{custom_time[1]}{custom_time[2]}{custom_time[3]}")
            month = int(f"{custom_time[5]}{custom_time[6]}")
            day = int(f"{custom_time[8]}{custom_time[9]}")
            hour = int(f"{custom_time[11]}{custom_time[12]}")
    
            date = datetime(year, month, day, hour)
    
    
        if hour == 0:  
            url = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                    f'&YEAR={date.strftime('%Y')}&MONTH={date.strftime('%m')}&FROM={date.strftime('%d')}0{hour}&TO={date.strftime('%d')}0{hour}'
                    f'&STNM={station_number}')
        else:
            url = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                    f'&YEAR={date.strftime('%Y')}&MONTH={date.strftime('%m')}&FROM={date.strftime('%d')}{hour}&TO={date.strftime('%d')}{hour}'
                    f'&STNM={station_number}')
    
        if proxies == None:
            response = requests.get(url, stream=True)
        else:
            response = requests.get(url, stream=True, proxies=proxies)
    
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            data = StringIO(soup.find_all('pre')[0].contents[0])
            success = True
        except Exception as e:
            success = False
    
        if success == False and current == True:
    
            date = new_date - timedelta(hours=12)
            hour = date.hour
    
            if hour == 0:  
                url = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                        f'&YEAR={date.strftime('%Y')}&MONTH={date.strftime('%m')}&FROM={date.strftime('%d')}0{hour}&TO={date.strftime('%d')}0{hour}'
                        f'&STNM={station_number}')
            else:
                url = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                        f'&YEAR={date.strftime('%Y')}&MONTH={date.strftime('%m')}&FROM={date.strftime('%d')}{hour}&TO={date.strftime('%d')}{hour}'
                        f'&STNM={station_number}')
        
            if proxies == None:
                response = requests.get(url, stream=True)
            else:
                response = requests.get(url, stream=True, proxies=proxies)
    
            try:
                soup = BeautifulSoup(response.content, "html.parser")
                data = StringIO(soup.find_all('pre')[0].contents[0])
                success = True
            except Exception as e:
                print(f"No Recent Sounding Data for {station_id}.\nQuitting Now")
                sys.exit()
        else:
            pass
            
                   
        col_names = ['PRES', 'HGHT', 'TEMP', 'DWPT', 'RELH', 'MIXR', 'DRCT', 'SKNT', 'THTA', 'THTE', 'THTV']
        df = pd.read_fwf(data, widths=[7] * 8, skiprows=5,
                             usecols=[0, 1, 2, 3, 6, 7], names=col_names)
        
        df['U-WIND'], df['V-WIND'] = get_u_and_v(df['SKNT'], df['DRCT'])
        df['RH'] = relative_humidity(df['TEMP'], df['DWPT'])
        pressure = df['PRES'].values * units('hPa')
        temperature = df['TEMP'].values * units('degC')
        df['THETA'] = mpcalc.potential_temperature(pressure, temperature)
        height = df['HGHT'].values * units('meters')
        theta = df['THETA'].values * units('degK')
        df['BVF'] = mpcalc.brunt_vaisala_frequency(height, theta, vertical_dim=0)
    
        return df

    else:
        date = now
        date_24 = date - timedelta(hours=24)
        if date.hour <= 12:
            hour = 00
        else:
            hour = 12

        y = date.year
        m = date.month
        d = date.day
        new_date = datetime(y, m, d, hour)
    
        if hour == 0:  
            url = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                    f'&YEAR={date.strftime('%Y')}&MONTH={date.strftime('%m')}&FROM={date.strftime('%d')}0{hour}&TO={date.strftime('%d')}0{hour}'
                    f'&STNM={station_number}')

            url_24 = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                    f'&YEAR={date.strftime('%Y')}&MONTH={date_24.strftime('%m')}&FROM={date_24.strftime('%d')}0{hour}&TO={date_24.strftime('%d')}0{hour}'
                    f'&STNM={station_number}')
            
        else:
            url = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                    f'&YEAR={date.strftime('%Y')}&MONTH={date.strftime('%m')}&FROM={date.strftime('%d')}{hour}&TO={date.strftime('%d')}{hour}'
                    f'&STNM={station_number}')

            url_24 = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                    f'&YEAR={date_24.strftime('%Y')}&MONTH={date_24.strftime('%m')}&FROM={date_24.strftime('%d')}{hour}&TO={date_24.strftime('%d')}{hour}'
                    f'&STNM={station_number}')
    
        if proxies == None:
            response = requests.get(url, stream=True)
            response_24 = requests.get(url_24, stream=True)
        else:
            response = requests.get(url, stream=True, proxies=proxies)
            response_24 = requests.get(url_24, stream=True, proxies=proxies)
    
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            soup_24 = BeautifulSoup(response_24.content, "html.parser")
            data = StringIO(soup.find_all('pre')[0].contents[0])
            data_24 = StringIO(soup_24.find_all('pre')[0].contents[0])
            success = True
        except Exception as e:
            success = False
    
        if success == False and current == True:
    
            date = new_date - timedelta(hours=12)
            date_24 = date - timedelta(hours=24)
            hour = date.hour
    
            if hour == 0:  
                url = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                        f'&YEAR={date.strftime('%Y')}&MONTH={date.strftime('%m')}&FROM={date.strftime('%d')}0{hour}&TO={date.strftime('%d')}0{hour}'
                        f'&STNM={station_number}')
    
                url_24 = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                        f'&YEAR={date.strftime('%Y')}&MONTH={date_24.strftime('%m')}&FROM={date_24.strftime('%d')}0{hour}&TO={date_24.strftime('%d')}0{hour}'
                        f'&STNM={station_number}')
                
            else:
                url = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                        f'&YEAR={date.strftime('%Y')}&MONTH={date.strftime('%m')}&FROM={date.strftime('%d')}{hour}&TO={date.strftime('%d')}{hour}'
                        f'&STNM={station_number}')
    
                url_24 = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                        f'&YEAR={date_24.strftime('%Y')}&MONTH={date_24.strftime('%m')}&FROM={date_24.strftime('%d')}{hour}&TO={date_24.strftime('%d')}{hour}'
                        f'&STNM={station_number}')
        
            if proxies == None:
                response = requests.get(url, stream=True)
                response_24 = requests.get(url_24, stream=True)
            else:
                response = requests.get(url, stream=True, proxies=proxies)
                response_24 = requests.get(url_24, stream=True, proxies=proxies)
    
            try:
                soup = BeautifulSoup(response.content, "html.parser")
                soup_24 = BeautifulSoup(response_24.content, "html.parser")
                data = StringIO(soup.find_all('pre')[0].contents[0])
                data_24 = StringIO(soup_24.find_all('pre')[0].contents[0])
                success = True
            except Exception as e:
                print(f"No Recent Sounding Data for {station_id}.\nQuitting Now")
                sys.exit()
        else:
            pass
            
                   
        col_names = ['PRES', 'HGHT', 'TEMP', 'DWPT', 'RELH', 'MIXR', 'DRCT', 'SKNT', 'THTA', 'THTE', 'THTV']
        df = pd.read_fwf(data, widths=[7] * 8, skiprows=5,
                             usecols=[0, 1, 2, 3, 6, 7], names=col_names)
        
        df['U-WIND'], df['V-WIND'] = get_u_and_v(df['SKNT'], df['DRCT'])
        df['RH'] = relative_humidity(df['TEMP'], df['DWPT'])
        pressure = df['PRES'].values * units('hPa')
        temperature = df['TEMP'].values * units('degC')
        df['THETA'] = mpcalc.potential_temperature(pressure, temperature)
        height = df['HGHT'].values * units('meters')
        theta = df['THETA'].values * units('degK')
        df['BVF'] = mpcalc.brunt_vaisala_frequency(height, theta, vertical_dim=0)

        df_24 = pd.read_fwf(data_24, widths=[7] * 8, skiprows=5,
                             usecols=[0, 1, 2, 3, 6, 7], names=col_names)
        
        df_24['U-WIND'], df_24['V-WIND'] = get_u_and_v(df_24['SKNT'], df_24['DRCT'])
        df_24['RH'] = relative_humidity(df_24['TEMP'], df_24['DWPT'])
        pressure_24 = df_24['PRES'].values * units('hPa')
        temperature_24 = df_24['TEMP'].values * units('degC')
        df_24['THETA'] = mpcalc.potential_temperature(pressure_24, temperature_24)
        height_24 = df_24['HGHT'].values * units('meters')
        theta_24 = df_24['THETA'].values * units('degK')
        df_24['BVF'] = mpcalc.brunt_vaisala_frequency(height_24, theta_24, vertical_dim=0)
    
        return df, df_24
















                               
