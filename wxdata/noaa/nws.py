"""
This file has the function that downloads NOAA/NWS and NOAA/SPC Forecast Data

(c) Eric J. Drewitz 2025
"""
# Import the needed libraries

import xarray as xr
import numpy as np
import os
import urllib.request
import warnings
warnings.filterwarnings('ignore')

from wxdata.utils.recycle_bin import *


alaska = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/'
conus = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
hawaii = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/'

def FIX_1D_GRIB_DATA(ds_short, 
                     ds_extended, 
                     varKey, 
                     short_term_fname, 
                     extended_fname):
    
    """
    This function fixes the NDFD Hawaii Grids. 
    Unfortunately, these grids are in 1-D when they need to be 2-D AND 
    the lon/lat keeps flipping which causes erroneous plots - so we will fix that!
    
    Required Arguments:
    
    1) ds_short (xarray data array) - The dataset of NDFD short-term GRIB Data. 
    
    2) ds_extended (xarray data array) - The dataset of NDFD extended GRIB Data. 
    
    3) varKey (String) - The key name of variable being exammined. 
    
    Variable names are also changed from their origional key value into plain language.
    
        Plain Language Variable Key List
        --------------------------------
        
        'maximum_relative_humidity'
        'mainimum_relative_humidity'
        'maximum_temperature'
        'minimum_temperature'
        'relative_humidity'
        'temperature'
        'apparent_temperature'
        'wind_speed'
        'wind_gust'
        'wind_direction'
        'spc_critical_fire_weather_forecast'
        'spc_dry_lightning_forecast'
        'spc_convective_outlook'
        'ice_accumulation'
        'probability_of_hail'
        '12_hour_probability_of_precipitation'
        'probability_of_extreme_tornadoes'
        'total_probability_of_severe_thunderstorms'
        'total_probability_of_extreme_severe_thunderstorms'
        'probability_of_extreme_thunderstorm_winds'
        'probability_of_extreme_hail'
        'probability_of_extreme_tornadoes'
        'probability_of_damaging_thunderstorm_winds'
        'quantitative_precipitation_forecast'
        'sky_cover'
        'snow_amount'
        'snow_level'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_cumulative'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_incremental'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_cumulative'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_incremental'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_cumulative'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_incremental'
        'dew_point'
        'visibility'
        'significant_wave_height'
        'warnings'
        'weather'       
        
    4) short_term_fname (String) - The filename of the short-term NDFD Grids. 
    
    5) extended_fname (String) - The filename of the extended NDFD Grids. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    A cleaned up xarray data array for the Hawaii grids. 
    """
    

    nrow = 225
    ncol = 321

    ds_list_short = []
    for i in range(0, len(ds_short['step']), 1):
        ds_short = ds_short.isel(step=i)
        
        var = ds_short[varKey].values
        lat = ds_short['latitude'].values
        lon = ds_short['longitude'].values
        
        var2d = np.empty([nrow,ncol])
        lat2d = np.empty([nrow,ncol])
        lon2d = np.empty([nrow,ncol])
        
        for i in range(0,nrow):
            start = i*ncol
            end = start+ncol
            if i%2==0:
                var2d[i,:] = var[start:end]
            else:
                var2d[i,:] = np.flip(var[start:end],axis=0)
            
            lat2d[i,:] = lat[start:end]
            lon2d[i,:] = lon[start:end]
        
        lon1d = lon2d[0,:]
        lat1d = lat2d[:,0]
        ds_list_short.append(var2d)
        ds_short = xr.open_dataset(f"NWS Data/{short_term_fname}", engine='cfgrib')
        data_var_names_1 = [var.name for var in ds_short.data_vars.values()]
        ds_short[varKey] = ds_short[data_var_names_1[0]]
        ds_short = ds_short.drop_vars(data_var_names_1[0])
        
    dims = ("step", "latitude", "longitude")
    short_coords = {
        "step": len(ds_list_short),
        "latitude": lat1d,  
        "longitude": lon1d,  
    }
    
    ds_short = xr.DataArray(ds_list_short, coords=short_coords, dims=dims)
        
    ds_list_extended = []
    for i in range(0, len(ds_extended['step']), 1):
        ds_extended = ds_extended.isel(step=i)
        
        var = ds_extended[varKey].values
        lat = ds_extended['latitude'].values
        lon = ds_extended['longitude'].values
        
        var2d = np.empty([nrow,ncol])
        lat2d = np.empty([nrow,ncol])
        lon2d = np.empty([nrow,ncol])
        
        for i in range(0,nrow):
            start = i*ncol
            end = start+ncol
            if i%2==0:
                var2d[i,:] = var[start:end]
            else:
                var2d[i,:] = np.flip(var[start:end],axis=0)
            
            lat2d[i,:] = lat[start:end]
            lon2d[i,:] = lon[start:end]
        
        lon1d = lon2d[0,:]
        lat1d = lat2d[:,0]
        ds_list_extended.append(var2d)
        ds_extended = xr.open_dataset(f"NWS Data/{extended_fname}", engine='cfgrib')
        data_var_names_1 = [var.name for var in ds_extended.data_vars.values()]
        ds_extended[varKey] = ds_extended[data_var_names_1[0]]
        ds_extended = ds_extended.drop_vars(data_var_names_1[0])
        
    dims = ("step", "latitude", "longitude")
    extended_coords = {
        "step": len(ds_list_extended),
        "latitude": lat1d,  
        "longitude": lon1d,  
    }
    
    ds_extended = xr.DataArray(ds_list_extended, coords=extended_coords, dims=dims)
    
    return ds_short, ds_extended

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
        'snow_level':'ds.snowlevel.bin',
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_cumulative':'ds.tcwspdabv34c.bin',
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_incremental':'ds.tcwspdabv34i.bin',  
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_cumulative':'ds.tcwspdabv50c.bin',
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_incremental':'ds.tcwspdabv50i.bin',   
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_cumulative':'ds.tcwspdabv64c.bin',
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_incremental':'ds.tcwspdabv64i.bin',
        'dew_point':'ds.td.bin',
        'visibility':'ds.vis.bin',
        'significant_wave_height':'ds.waveh.bin',
        'warnings':'ds.wwa.bin',
        'weather':'ds.wx.bin'
        
    }
    
    return parameters[parameter]


def get_ndfd_grids(parameter, 
                   state,
                   clear_recycle_bin=True):

    """

    This function retrieves the latest NWS Forecast (NDFD) files from the NWS FTP Server. 

    Data Source: NOAA/NWS/NDFD (tgftp.nws.noaa.gov)

    Required Arguments: 

    1) parameter (String) - The parameter that the user wishes to download. 
    
    Parameters
    ----------
    
    'maximum_relative_humidity'
    'mainimum_relative_humidity'
    'maximum_temperature'
    'minimum_temperature'
    'relative_humidity'
    'temperature'
    'apparent_temperature'
    'wind_speed'
    'wind_gust'
    'wind_direction'
    'spc_critical_fire_weather_forecast'
    'spc_dry_lightning_forecast'
    'spc_convective_outlook'
    'ice_accumulation'
    'probability_of_hail'
    '12_hour_probability_of_precipitation'
    'probability_of_extreme_tornadoes'
    'total_probability_of_severe_thunderstorms'
    'total_probability_of_extreme_severe_thunderstorms'
    'probability_of_extreme_thunderstorm_winds'
    'probability_of_extreme_hail'
    'probability_of_extreme_tornadoes'
    'probability_of_damaging_thunderstorm_winds'
    'quantitative_precipitation_forecast'
    'sky_cover'
    'snow_amount'
    'snow_level'
    'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_cumulative'
    'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_incremental'
    'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_cumulative'
    'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_incremental'
    'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_cumulative'
    'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_incremental'
    'dew_point'
    'visibility'
    'significant_wave_height'
    'warnings'
    'weather'  

    2) state (String) - The state or region being used. 
    
    Optional Arguments: 
    
    1) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 

    Returns
    -------
    
    An xarray.data array of the latest NWS/SPC Forecast data.
    
    Variable names are also changed from their origional key value into plain language.
    
        Plain Language Variable Key List
        --------------------------------
        
        'maximum_relative_humidity'
        'mainimum_relative_humidity'
        'maximum_temperature'
        'minimum_temperature'
        'relative_humidity'
        'temperature'
        'apparent_temperature'
        'wind_speed'
        'wind_gust'
        'wind_direction'
        'spc_critical_fire_weather_forecast'
        'spc_dry_lightning_forecast'
        'spc_convective_outlook'
        'ice_accumulation'
        'probability_of_hail'
        '12_hour_probability_of_precipitation'
        'probability_of_extreme_tornadoes'
        'total_probability_of_severe_thunderstorms'
        'total_probability_of_extreme_severe_thunderstorms'
        'probability_of_extreme_thunderstorm_winds'
        'probability_of_extreme_hail'
        'probability_of_extreme_tornadoes'
        'probability_of_damaging_thunderstorm_winds'
        'quantitative_precipitation_forecast'
        'sky_cover'
        'snow_amount'
        'snow_level'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_cumulative'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_incremental'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_cumulative'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_incremental'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_cumulative'
        'probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_incremental'
        'dew_point'
        'visibility'
        'significant_wave_height'
        'warnings'
        'weather'       

    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    state = state.upper()

    if state == 'AK': 
        directory_name = alaska
    elif state == 'HI':
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
    
    if state == 'HI':
        
        ds1, ds2 = FIX_1D_GRIB_DATA(ds1, ds2, parameter, short_term_fname, extended_fname)
        
    else:
        pass

    return ds1, ds2
