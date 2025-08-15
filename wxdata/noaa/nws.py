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

    if parameter == 'ds.maxrh.bin':
        short_term_fname = 'ds.maxrh_short.bin'
        extended_fname = 'ds.maxrh_extended.bin'

    if parameter == 'ds.minrh.bin':
        short_term_fname = 'ds.minrh_short.bin'
        extended_fname = 'ds.minrh_extended.bin'

    if parameter == 'ds.maxt.bin':
        short_term_fname = 'ds.maxt_short.bin'
        extended_fname = 'ds.maxt_extended.bin'

    if parameter == 'ds.mint.bin':
        short_term_fname = 'ds.mint_short.bin'
        extended_fname = 'ds.mint_extended.bin'

    if parameter == 'ds.rhm.bin':
        short_term_fname = 'ds.rhm_short.bin'
        extended_fname = 'ds.rhm_extended.bin'    

    if parameter == 'ds.temp.bin':
        short_term_fname = 'ds.temp_short.bin'
        extended_fname = 'ds.temp_extended.bin' 

    if parameter == 'ds.wspd.bin':
        short_term_fname = 'ds.wspd_short.bin'
        extended_fname = 'ds.wspd_extended.bin'  

    if parameter == 'ds.wgust.bin':
        short_term_fname = 'ds.wgust_short.bin'
        extended_fname = 'ds.wgust_extended.bin'   

    if parameter == 'ds.wdir.bin':
        short_term_fname = 'ds.wdir_short.bin'
        extended_fname = 'ds.wdir_extended.bin'  

    if parameter == 'ds.critfireo.bin':
        short_term_fname = 'ds.critfireo_short.bin'
        extended_fname = 'ds.critfireo_extended.bin'     

    if parameter == 'ds.dryfireo.bin':
        short_term_fname = 'ds.dryfireo_short.bin'
        extended_fname = 'ds.dryfireo_extended.bin' 

    if parameter == 'ds.conhazo.bin':
        short_term_fname = 'ds.conhazo_short.bin'
        extended_fname = 'ds.conhazo_extended.bin' 


    if os.path.exists(short_term_fname):
        os.remove(short_term_fname)
        urllib.request.urlretrieve(f"https://tgftp.nws.noaa.gov{directory_name}VP.001-003/{parameter}", f"{parameter}")
        os.rename(parameter, short_term_fname)
    else:
        urllib.request.urlretrieve(f"https://tgftp.nws.noaa.gov{directory_name}VP.001-003/{parameter}", f"{parameter}")
        os.rename(parameter, short_term_fname)
    
    if os.path.exists(extended_fname):
        try:
            os.remove(extended_fname)
            urllib.request.urlretrieve(f"https://tgftp.nws.noaa.gov{directory_name}VP.004-007/{parameter}", f"{parameter}")
            os.rename(parameter, extended_fname)
            extended = True
        except Exception as e:
            extended = False
    else:
        try:
            urllib.request.urlretrieve(f"https://tgftp.nws.noaa.gov{directory_name}VP.004-007/{parameter}", f"{parameter}")
            os.rename(parameter, extended_fname)
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

    return ds1, ds2
