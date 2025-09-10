"""
This file has the function that downloads NOAA/NWS and NOAA/SPC Forecast Data

(c) Eric J. Drewitz 2025
"""
# Import the needed libraries

import xarray as xr
import os
import urllib.request
import warnings
warnings.filterwarnings('ignore')

from wxdata.utils.recycle_bin import *
clear_recycle_bin_windows()
clear_trash_bin_mac()
clear_trash_bin_linux()


alaska = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/'
conus = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
hawaii = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/'

def get_parameters(parameter):
    
    """
    This function returns the filename for a given NDFD Weather Element. 
    
    Required Arguments:
    
    1) parameter (String) - The parameter name as a string. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    The filename for a given parameter. 
    """
    
    parameters = {
        
        'maximum_relative_humidity':'ds.maxrh.bin',
        'mainimum_relative_humidity':'ds.minrh.bin',
        'maximum_temperature':'ds.maxt.bin',
        'minimum_temperature':'ds.mint.bin',
        'relative_humidity':'ds.rhm.bin',
        'temperature':'ds.temp.bin',
        'apparent_temperature':'ds.apt.bin',
        'wind_speed':'ds.wspd.bin',
        'wind_gust':'ds.wgust.bin',
        'wind_direction':'ds.wdir.bin',
        'spc_critical_fire_weather_forecast':'ds.critfireo.bin',
        'spc_dry_lightning_forecast':'ds.dryfireo.bin',
        'spc_convective_outlook':'ds.conhazo.bin',
        'ice_accumulation':'ds.iceaccum.bin',
        'probability_of_hail':'ds.phail.bin',
        '12_hour_probability_of_precipitation':'ds.pop12.bin',
        'probability_of_extreme_tornadoes':'ds.ptornado.bin',
        'total_probability_of_severe_thunderstorms':'ds.ptotsvrtstm.bin',
        'total_probability_of_extreme_severe_thunderstorms':'ds.ptotxsvrtstm.bin',
        'probability_of_extreme_thunderstorm_winds':'ds.pxtstmwinds.bin',
        'probability_of_extreme_hail':'ds.pxhail.bin',
        'probability_of_extreme_tornadoes':'ds.pxtornado.bin',
        'probability_of_damaging_thunderstorm_winds':'ds.ptstmwinds.bin',
        'quantitative_precipitation_forecast':'ds.qpf.bin',
        'sky_cover':'ds.sky.bin',
        'snow_amount':'ds.snow.bin',
        'snow_level':'ds.snowlevel.bin'       
        
        
        
    }
    
    return parameters[parameter]


def get_ndfd_grids(parameter, state):

    """

    This function retrieves the latest NWS Forecast (NDFD) files from the NWS FTP Server. 

    Data Source: NOAA/NWS/NDFD (tgftp.nws.noaa.gov)

    Required Arguments: 
    
    1) directory_name (String) - The name of the directory (see FireWxPy documentation for directory paths)

    2) parameter (String) - The parameter that the user wishes to download. (i.e. ds.maxt.bin for max temperature)

    3) state (String) - The state or region being used. 

    Returns: An xarray.data_array of the latest NWS/SPC Forecast data

    """

    if state == 'AK' or state == 'ak': 
        directory_name = alaska
    elif state == 'HI' or state == 'hi':
        directory_name = hawaii
    else:
        directory_name = conus
        
    parameter = parameter

    if os.path.exists(f"NWS Data"):
        pass
    else:
        os.mkdir(f"NWS Data")

    for file in os.listdir(f"NWS Data"):
        try:
            os.remove(f"NWS Data"/{file})
        except Exception as e:
            pass

    fname = get_parameters(parameter)

    short_term_fname = f"ds.{parameter}_short.bin"
    extended_fname = f"ds.{parameter}_extended.bin"


    if os.path.exists(short_term_fname):
        os.remove(short_term_fname)
        urllib.request.urlretrieve(f"https://tgftp.nws.noaa.gov{directory_name}VP.001-003/{fname}", f"{fname}")
        os.rename(fname, short_term_fname)
    else:
        urllib.request.urlretrieve(f"https://tgftp.nws.noaa.gov{directory_name}VP.001-003/{fname}", f"{fname}")
        os.rename(fname, short_term_fname)
    
    if os.path.exists(extended_fname):
        try:
            os.remove(extended_fname)
            urllib.request.urlretrieve(f"https://tgftp.nws.noaa.gov{directory_name}VP.004-007/{fname}", f"{fname}")
            os.rename(fname, extended_fname)
            extended = True
        except Exception as e:
            extended = False
    else:
        try:
            urllib.request.urlretrieve(f"https://tgftp.nws.noaa.gov{directory_name}VP.004-007/{fname}", f"{fname}")
            os.rename(fname, extended_fname)
            extended = True
        except Exception as e:
            extended = False

    os.replace(short_term_fname, f"NWS Data/{short_term_fname}")
    try:
        os.replace(extended_fname, f"NWS Data/{extended_fname}")
    except Exception as e:
        pass

    short_path = f"NWS Data/{short_term_fname}"
    try:
        extended_path = f"NWS Data/{extended_fname}"
    except Exception as e:
        pass

    try:
        os.remove(parameter)
    except Exception as e:
        pass

    if state != 'AK' or state != 'ak' or state == None:
        ds1 = xr.open_dataset(short_path, engine='cfgrib', decode_timedelta=False)
    else:
        ds1 = xr.open_dataset(short_path, engine='cfgrib', decode_timedelta=False).sel(x=slice(20, 1400, 2), y=slice(100, 1400, 2)) 
    try:
        if ds1['time'][1] == True:
            ds1 = ds1.isel(time=1)
        else:
            ds1 = ds1.isel(time=0)
    except Exception as e:
        try:
            ds1 = ds1.isel(time=0)
        except Exception as e:
            ds1 = ds1

    if extended == True:
        try:

            if state != 'AK' or state != 'ak' or state == None:
                ds2 = xr.open_dataset(extended_path, engine='cfgrib', decode_timedelta=False)
            else:
                ds2 = xr.open_dataset(extended_path, engine='cfgrib', decode_timedelta=False).sel(x=slice(20, 1400, 2), y=slice(100, 1400, 2)) 
    
            try:
                if ds2['time'][1] == True:
                        ds2 = ds2.isel(time=1)
                else:
                    ds2 = ds2.isel(time=0)  
            except Exception as e:
                try:
                    ds2 = ds2.isel(time=0)
                except Exception as e:
                    ds2 = ds2
        except Exception as e:
            pass
    else:
        ds2 = False
        
    ds1 = ds1.metpy.parse_cf()

    if extended == True:
        try:
            ds2 = ds2.metpy.parse_cf() 
        except Exception as e:
            ds2 = False
    else:
        pass

    for item in os.listdir(f"NWS Data"):
        if item.endswith(".idx"):
            os.remove(f"NWS Data/{item}")
        
    print(f"Retrieved {parameter} NDFD grids.")
    
    data_var_names_1 = [var.name for var in ds1.data_vars.values()]
    ds1[parameter] = ds1[data_var_names_1[0]]
    ds1 = ds1.drop_vars(data_var_names_1[0])
    
    data_var_names_2 = [var.name for var in ds2.data_vars.values()]
    ds2[parameter] = ds2[data_var_names_2[0]]
    ds2 = ds2.drop_vars(data_var_names_2[0])

    return ds1, ds2
