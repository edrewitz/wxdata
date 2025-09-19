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

from wxdata.calc.thermodynamics import(

    relative_humidity,
    saturation_vapor_pressure
)

from wxdata.calc.kinematics import get_u_and_v
from metpy.units import units
from bs4 import BeautifulSoup
from io import StringIO

from wxdata.utils.recycle_bin import *
clear_recycle_bin_windows()
clear_trash_bin_mac()
clear_trash_bin_linux()

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
    
    To find the list of station IDs, visit: https://weather.uwyo.edu/upperair/sounding_legacy.html

    Returns
    -------

    An integer for the station number
    """

    station_id = station_id.upper()

    station_ids = {

        'PABR':'70026',
        'PAOM':'70200',
        'PAMC':'70231',
        'PAYA':'70361',
        'PANT':'70398',
        'PAVA':'70361',
        'NKX':'72293',
        'OTX':'72786',
        'SLE':'72694',
        'MFR':'72597',
        'OAK':'72493',
        'VEF':'72388',
        'REV':'72489',
        'BOI':'72681',
        'LKN':'72582',
        'SLC':'72572',
        'TUS':'72274',
        'EPZ':'72364',
        'GJT':'72476',
        'RIW':'72672',
        'GGW':'72768',
        'BIS':'72764',
        'UNR':'72662',
        'ABQ':'72365',
        'MAF':'72265',
        'DRT':'72261',
        'MMAN':'76394',
        'CRP':'72251',
        'BRO':'72250',
        'FWD':'72249',
        'AMA':'72363',
        'OUN':'72357',
        'DDC':'72451',
        'TOP':'72456',
        'LBF':'72562',
        'OAX':'72558',
        'ABR':'72659',
        'INL':'72747',
        'MPX':'72649',
        'SGF':'72440',
        'LZK':'72340',
        'SHV':'72248',
        'LCH':'72240',
        'LIX':'72233',
        'JAN':'72235',
        'VBG':'72393',
        'YEV':'71957',
        'YVQ':'71043',
        'ZXS':'71908',
        'YZT':'71109',
        'CWVK':'73033',
        'YQD':'71867',
        'YBK':'71926',
        'YCB':'71925',
        'YRB':'71924',
        'YUX':'71081',
        'YFB':'71909',
        'YVP':'71906',
        'YAH':'71823',
        'YZV':'71811',
        'YYR':'71816',
        'YJT':'71815',
        'AYT':'71802',
        'BGEM':'04220',
        'BGBW':'04270',
        'TXKF':'78016',
        'CAR':'72712',
        'YQI':'71603',
        'GYX':'74389',
        'ALB':'72518',
        'WMW':'71722',
        'BUF':'72528',
        'OKX':'72501',
        'DTX':'72632',
        'APX':'72634',
        'GRB':'72645',
        'ILX':'74560',
        'ILN':'72426',
        'BNA':'72327',
        'BNF':'72800',
        'FFC':'72215',
        'BMX':'72230',
        'PIT':'72520',
        'IAD':'72403',
        'WAL':'72402',
        'RNK':'72318',
        'GSO':'72317',
        'MHX':'72305',
        'CHS':'72208',
        'JAX':'72206',
        'TBW':'72210',
        'EYW':'72201',
        'SKSP':'80001',
        'MPCZ':'78807',
        'SKBQ':'80028',
        'SKBG':'80094',
        'MKJP':'78397',
        'MDSD':'78486',
        'TJSJ':'78526',
        'TBPB':'78954',
        'SBBV':'82022',
        'SBMQ':'82099',
        'SBBE':'82193',
        'SBMN':'82332',
        'SKLT':'80398',
        'SBPV':'82824',
        'SBNT':'82599',
        'SBAT':'82965',
        'SBVH':'83208',
        'SCFA':'85442',
        'SBBR':'83378',
        'SBUL':'83525',
        'SBCG':'83612',
        'SBLO':'83768',
        'SBMT':'83779',
        'SBCT':'83840',
        'SBCT':'83840',
        'SBFL':'83899',
        'SBFI':'83827',
        'SGAS':'86218',
        'SARE':'87155',
        'SBUG':'83928',
        'SBSM':'83937',
        'SACO':'87344',
        'SAME':'87418',
        'SCSN':'85586',
        'SAZR':'87623',
        'SAZN':'87715',
        'SCTE':'85799',
        'SAVC':'87860',
        'SCCI':'85934',
        'PHTO':'91285',
        'PHLI':'91165',
        'PKMJ':'91376',
        'RJAM':'47991',
        'RJAO':'47971',
        'ROMD':'47945',
        'ROIG':'47918',
        'RPLI':'98223',
        'PGUM':'91212',
        'PTPN':'91348',
        'PTKK':'91334',
        'PTYA':'91413',
        'PTRO':'91408',
        'RPMP':'98444',
        'RPVG':'98558',
        'RPMT':'98646',
        'RPVP':'98618',
        'RPMD':'98753',
        'WBKK':'96471',
        'WBKW':'96481',
        'WRLR':'96509',
        'WBGB':'96441',
        'WBGG':'96413',
        'WASS':'97502',
        'WAAA':'97180',
        'WRSJ':'96935',
        'WRRR':'97230',
        'WRKK':'97372',
        'YPDN':'94120',
        'YBRM':'94203',
        'YPPD':'94312',
        'YPLM':'94302',
        'YPGN':'94403',
        'YPPH':'94610',
        'YPAL':'94802',
        'YPDN':'94120',
        'YPWR':'94659',
        'YPAD':'94672',
        'YMML':'94866',
        'YSWG':'94910',
        'YBCV':'94510',
        'YBBN':'94578',
        'NGFU':'91643',
        'NFFN':'91680',
        'YSNF':'94996',
        'NZWP':'93112',
        'NZPP':'93417',
        'NZNV':'93844',
        'WEU':'71917',
        'WLT':'71082',
        'BGDH':'04320',
        'BGSC':'04339',
        'BIKF':'04018',
        'ENJA':'01001',
        'ENOL':'01241',
        'ULOL':'26477',
        'ULWW':'27038',
        'UUOO':'34122',
        'UWPP':'27962',
        'URWW':'34467',
        'UATT':'35229',
        'USHH':'23933',
        'UNNN':'29634',
        'UNII':'29263',
        'UINN':'29698',
        'UIAA':'30758',
        'UEEE':'24959',
        'UHMM':'25913',
        'UHPP':'32540',
        'EDZE':'10410',
        'LIMN':'16064',
        'LIED':'16546',
        'LICT':'16429',
        'LIRE':'16245',
        'LIBN':'16332',
        'LIPI':'16045',
        'LDDD':'14240',
        'LHUD':'12982',
        'LYNI':'13388',
        'LBSF':'15614',
        'LGAT':'16716',
        'LRBS':'15420',
        'LTBM':'17240',
        'LTAU':'17196',
        'DTTZ':'60760',
        'DRZA':'61024',
        'DRRN':'61052',
        'DFFD':'65503',
        'DIMN':'65548',
        'FAIR':'68263',
        'ERZM':'17095',
        'OITT':'40706',
        'OING':'40738',
        'OIMB':'40809',
        'OIKK':'40841',
        'OIAW':'40811',
        'OEPA':'40373',
        'OEHL':'40394',
        'OEMA':'40430',
        'OEAB':'41112',
        'OERK':'40437',
        'OEDF':'40417',
        'OMAA':'41217',
        'VAAH':'42647',
        'VABB':'43003',
        'VOCC':'43353',
        'VOMM':'43279',
        'VANP':'42867',
        'VIDD':'42182',
        'VILK':'42369',
        'VEJH':'42886',
        'VECC':'42809',
        'VEAT':'42724',
        'VGTJ':'41923',
        'VEGT':'42410',
        'VVNB':'48820',
        'VTCC':'48327',
        'VTPS':'48378',
        'VTUK':'48381',
        'VTUU':'48407',
        'VVDN':'48855',
        'VVTS':'48900',
        'VTUN':'48431',
        'VTBC':'48480',
        'VTPB':'48500',
        'WMKP':'48601',
        'WIMM':'96035',
        'WIII':'96749',
        'WRSJ':'96935',
        'WRRR':'97230'
        

    }

    station_number = station_ids.get(station_id)

    return station_number
    

def get_observed_sounding_data(station_id, current=True, custom_time=None, comparison_24=False, proxies=None):

    """
    This function scrapes the University of Wyoming Sounding Database and returns the data in a Pandas DataFrame

    Required Arguments:

    1) station_id (String or Integer) - User inputs the station_id as a string or an integer. 
    Some stations only have the ID by integer. Please see https://weather.uwyo.edu/upperair/sounding_legacy.html for more info. 

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
            date = datetime(y, m, d, hour)
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
    
        max_retries = 5
        retry = 0
        if proxies == None:
            response = requests.get(url, stream=True)
            while response.status_code != 200:
                response = requests.get(url, stream=True)
                retry = retry + 1
                if retry > max_retries:
                    break
        else:
            response = requests.get(url, stream=True, proxies=proxies)
            while response.status_code != 200:
                response = requests.get(url, stream=True, proxies=proxies)
                retry = retry + 1
                if retry > max_retries:
                    break    
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            data = StringIO(soup.find_all('pre')[0].contents[0])
            success = True
        except Exception as e:
            success = False
    
        if success == False and current == True:
    
            date = date - timedelta(hours=12)
            hour = date.hour
    
            if hour == 0:  
                url = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                        f'&YEAR={date.strftime('%Y')}&MONTH={date.strftime('%m')}&FROM={date.strftime('%d')}0{hour}&TO={date.strftime('%d')}0{hour}'
                        f'&STNM={station_number}')
            else:
                url = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
                        f'&YEAR={date.strftime('%Y')}&MONTH={date.strftime('%m')}&FROM={date.strftime('%d')}{hour}&TO={date.strftime('%d')}{hour}'
                        f'&STNM={station_number}')
        
            max_retries = 5
            retry = 0
            if proxies == None:
                response = requests.get(url, stream=True)
                while response.status_code != 200:
                    response = requests.get(url, stream=True)
                    retry = retry + 1
                    if retry > max_retries:
                        break
            else:
                response = requests.get(url, stream=True, proxies=proxies)
                while response.status_code != 200:
                    response = requests.get(url, stream=True, proxies=proxies)
                    retry = retry + 1
                    if retry > max_retries:
                        break    
    
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
    
        return df, date

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
        date = datetime(y, m, d, hour)
    
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

        max_retries = 5
        retry = 0
        if proxies == None:
            response = requests.get(url, stream=True)
            response_24 = requests.get(url_24, stream=True)
            while response.status_code != 200 and response_24.status_code != 200:
                response = requests.get(url, stream=True)
                response_24 = requests.get(url_24, stream=True)
                retry = retry + 1
                if retry > max_retries:
                    break
        else:
            response = requests.get(url, stream=True, proxies=proxies)
            response_24 = requests.get(url_24, stream=True, proxies=proxies)
            while response.status_code != 200 and response_24.status_code != 200:
                response = requests.get(url, stream=True, proxies=proxies)
                response_24 = requests.get(url_24, stream=True, proxies=proxies)
                retry = retry + 1
                if retry > max_retries:
                    break
    
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            soup_24 = BeautifulSoup(response_24.content, "html.parser")
            data = StringIO(soup.find_all('pre')[0].contents[0])
            data_24 = StringIO(soup_24.find_all('pre')[0].contents[0])
            success = True
        except Exception as e:
            success = False
    
        if success == False and current == True:
    
            date = date - timedelta(hours=12)
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
        
            max_retries = 5
            retry = 0
            if proxies == None:
                response = requests.get(url, stream=True)
                response_24 = requests.get(url_24, stream=True)
                while response.status_code != 200 and response_24.status_code != 200:
                    response = requests.get(url, stream=True)
                    response_24 = requests.get(url_24, stream=True)
                    retry = retry + 1
                    if retry > max_retries:
                        break
            else:
                response = requests.get(url, stream=True, proxies=proxies)
                response_24 = requests.get(url_24, stream=True, proxies=proxies)
                while response.status_code != 200 and response_24.status_code != 200:
                    response = requests.get(url, stream=True, proxies=proxies)
                    response_24 = requests.get(url_24, stream=True, proxies=proxies)
                    retry = retry + 1
                    if retry > max_retries:
                        break
    
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
    
        return df, df_24, date, date_24
















                               
