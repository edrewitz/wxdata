"""
This file hosts the function that preprocesses RTMA Data. 

(C) Eric J. Drewitz 2025
"""
    
import xarray as xr
import numpy as np
import metpy.calc as mpcalc
import sys
import logging
import warnings
warnings.filterwarnings('ignore')

from wxdata.calc.thermodynamics import relative_humidity
from wxdata.utils.file_funcs import clear_idx_files_in_path

sys.tracebacklimit = 0
logging.disable()

def rows_and_cols(model):
    
    """
    This function returns the number of rows and columns for the low-latitude island RTMA datasets.
    
    This is needed to resolve the "1-D Data Problem" in these datasets. 
    
    Required Arguments: 
    
    1) model (String) - Default='rtma'. The RTMA model being used:
    
    RTMA Models
    -----------
    
    Hawaii = 'hi rtma'
    Puerto Rico = 'pr rtma'
    Guam = 'gu rtma'
    
    Optional Arguments: None
    
    Returns
    -------
    
    The number of rows and columns for post-processing the 1-D RTMA Datasets    
    """
    model = model.upper()
    
    dims = {
        
        'HI RTMA':[225, 321],
        'PR RTMA':[176, 251],
        'GU RTMA':[193, 193]
    }
    
    return dims[model][0], dims[model][1]

def process_rtma_data(filename, 
                     model,
                     directory):
    
    """
    This function post-processes RTMA Data and returns an xarray data array of the data.
    
    This post-processing will convert all variable names into a plain language format. 
    
    
    Required Arguments: 
    
    1) path (String) - The path to the file that has the RTMA Data. 
    
    2) model (String) - Default='rtma'. The RTMA model being used:
    
    RTMA Models
    -----------
    
    CONUS = 'rtma'
    Alaska = 'ak rtma'
    Hawaii = 'hi rtma'
    Puerto Rico = 'pr rtma'
    Guam = 'gu rtma'
    
    3) directory (String) - The directory path where the RTMA files are saved to. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray data array of the RTMA Dataset with variable keys converted from the GRIB format to a Plain Language format. 
    
    Variable Keys
    -------------
    
    'orography'
    'surface_pressure'
    '2m_temperature'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_specific_humidity'
    'surface_visibility'
    'cloud_ceiling_height'
    'total_cloud_cover'
    '10m_u_wind_component'
    '10m_v_wind_component'
    '10m_wind_direction'
    '10m_wind_speed'
    '10m_wind_gust'
        
    """
    model = model.upper()
    
    clear_idx_files_in_path(directory)
    
    filepath = f"{directory}/{filename}"

    ds = xr.open_dataset(f"{filepath}", engine='cfgrib')
    
    ds['orography'] = ds['orog']
    ds['surface_pressure'] = ds['sp']
    ds['2m_temperature'] = ds['t2m']
    ds['2m_dew_point'] = ds['d2m']
    ds['2m_relative_humidity'] = relative_humidity(ds['2m_temperature'], ds['2m_dew_point'])
    ds['2m_specific_humidity'] = ds['sh2']
    ds['surface_visibility'] = ds['vis']
    ds['cloud_ceiling_height'] = ds['ceil']
    ds['total_cloud_cover'] = ds['tcc']
    
    ds = ds.drop_vars(
        
        ['orog',
         'sp',
         't2m',
         'd2m',
         'sh2',
         'vis',
         'ceil',
         'tcc']
    )
    

    ds1 = xr.open_dataset(f"{filepath}", 
                          engine='cfgrib', 
                          decode_timedelta=False, 
                          filter_by_keys={'typeOfLevel': 'heightAboveGround','shortName':'10u'})
    ds['10m_u_wind_component'] = ds1['u10']
    
    ds2 = xr.open_dataset(f"{filepath}", 
                          engine='cfgrib', 
                          decode_timedelta=False, 
                          filter_by_keys={'typeOfLevel': 'heightAboveGround','shortName':'10v'})
    ds['10m_v_wind_component'] = ds2['v10']    
    

    ds3 = xr.open_dataset(f"{filepath}", 
                          engine='cfgrib', 
                          decode_timedelta=False, 
                          filter_by_keys={'typeOfLevel': 'heightAboveGround','shortName':'10wdir'})
    ds['10m_wind_direction'] = ds3['wdir10']
    

    ds4 = xr.open_dataset(f"{filepath}", 
                          engine='cfgrib', 
                          decode_timedelta=False, 
                          filter_by_keys={'typeOfLevel': 'heightAboveGround','shortName':'10si'})
    ds['10m_wind_speed'] = ds4['si10']
    

    ds5 = xr.open_dataset(f"{filepath}",
                          engine='cfgrib',
                          decode_timedelta=False, 
                          filter_by_keys={'typeOfLevel': 'heightAboveGround','shortName':'i10fg'})
    ds['10m_wind_gust'] = ds5['i10fg']
    
    if model == 'HI RTMA' or model == 'GU RTMA' or model == 'PR RTMA':
        
        nrows, ncols = rows_and_cols(model)
        
        orog = ds['orography'].values
        pressure = ds['surface_pressure'].values
        temp = ds['2m_temperature'].values
        dwpt = ds['2m_dew_point'].values
        rh = ds['2m_relative_humidity'].values
        sh = ds['2m_specific_humidity'].values
        vis = ds['surface_visibility'].values
        ceil = ds['cloud_ceiling_height'].values
        tcc = ds['total_cloud_cover'].values
        u = ds['10m_u_wind_component'].values
        v = ds['10m_v_wind_component'].values
        wdir = ds['10m_wind_direction'].values
        ws = ds['10m_wind_speed'].values
        wgust = ds['10m_wind_gust'].values
        lat = ds['latitude'].values
        lon = ds['longitude'].values
        time = ds['time'].values

        orog_2d = np.empty([nrows,ncols])
        pressure_2d = np.empty([nrows,ncols])
        temp_2d = np.empty([nrows,ncols])
        dwpt_2d = np.empty([nrows,ncols])
        rh_2d = np.empty([nrows,ncols])
        sh_2d = np.empty([nrows,ncols])
        vis_2d = np.empty([nrows,ncols])
        ceil_2d = np.empty([nrows,ncols])
        tcc_2d = np.empty([nrows,ncols])
        u_2d = np.empty([nrows,ncols])
        v_2d = np.empty([nrows,ncols])
        wdir_2d = np.empty([nrows,ncols])
        ws_2d = np.empty([nrows,ncols])
        wgust_2d = np.empty([nrows,ncols])
        lat_2d = np.empty([nrows,ncols])
        lon_2d = np.empty([nrows,ncols])    
        
        for i in range(0,nrows):
            start = i*ncols
            end = start+ncols

            orog_2d[i,:] = orog[start:end]
            pressure_2d[i,:] = pressure[start:end]
            temp_2d[i,:] = temp[start:end]
            dwpt_2d[i,:] = dwpt[start:end]
            rh_2d[i,:] = rh[start:end]
            sh_2d[i,:] = sh[start:end]
            vis_2d[i,:] = vis[start:end]
            ceil_2d[i,:] = ceil[start:end]
            tcc_2d[i,:] = tcc[start:end]
            u_2d[i,:] = u[start:end]
            v_2d[i,:] = v[start:end]
            wdir_2d[i,:] = wdir[start:end]
            ws_2d[i,:] = ws[start:end]
            wgust_2d[i,:] = wgust[start:end]


            lat_2d[i,:] = lat[start:end]
            lon_2d[i,:] = lon[start:end]

        lon1d = lon_2d[0,:]
        lat1d = lat_2d[:,0]  
        
        dims = ("latitude", "longitude")
        coords = {
            "time":time,
            "latitude": lat1d,  
            "longitude": lon1d,  
        }
        
        ds1 = xr.DataArray(orog_2d, coords=coords, dims=dims)
        ds2 = xr.DataArray(pressure_2d, coords=coords, dims=dims)
        ds3 = xr.DataArray(temp_2d, coords=coords, dims=dims)
        ds4 = xr.DataArray(dwpt_2d, coords=coords, dims=dims)
        ds5 = xr.DataArray(rh_2d, coords=coords, dims=dims)
        ds6 = xr.DataArray(sh_2d, coords=coords, dims=dims)
        ds7 = xr.DataArray(vis_2d, coords=coords, dims=dims)
        ds8 = xr.DataArray(ceil_2d, coords=coords, dims=dims)
        ds9 = xr.DataArray(tcc_2d, coords=coords, dims=dims)
        ds10 = xr.DataArray(u_2d, coords=coords, dims=dims)
        ds11 = xr.DataArray(v_2d, coords=coords, dims=dims)
        ds12 = xr.DataArray(wdir_2d, coords=coords, dims=dims)
        ds13 = xr.DataArray(ws_2d, coords=coords, dims=dims)
        ds14 = xr.DataArray(wgust_2d, coords=coords, dims=dims)
        
        ds1['orography'] = ds1
        ds1['surface_pressure'] = ds2
        ds1['2m_temperature'] = ds3
        ds1['2m_dew_point'] = ds4
        ds1['2m_relative_humidity'] = ds5
        ds1['2m_specific_humidity'] = ds6
        ds1['surface_visibility'] = ds7
        ds1['cloud_ceiling_height'] = ds8
        ds1['total_cloud_cover'] = ds9
        ds1['10m_u_wind_component'] = ds10
        ds1['10m_v_wind_component'] = ds11
        ds1['10m_wind_direction'] = ds12
        ds1['10m_wind_speed'] = ds13
        ds1['10m_wind_gust'] = ds14
        
        ds1['surface_pressure'] = mpcalc.smooth_gaussian(ds1['surface_pressure'], n=8)
        ds1['2m_temperature'] = mpcalc.smooth_gaussian(ds1['2m_temperature'], n=8)
        ds1['2m_dew_point'] = mpcalc.smooth_gaussian(ds1['2m_dew_point'], n=8)
        ds1['2m_relative_humidity'] = mpcalc.smooth_gaussian(ds1['2m_relative_humidity'], n=8)
        ds1['2m_specific_humidity'] = mpcalc.smooth_gaussian(ds1['2m_specific_humidity'], n=8)
        ds1['surface_visibility'] = mpcalc.smooth_gaussian(ds1['surface_visibility'], n=8)
        ds1['cloud_ceiling_height'] = mpcalc.smooth_gaussian(ds1['cloud_ceiling_height'], n=8)
        ds1['total_cloud_cover'] = mpcalc.smooth_gaussian(ds1['total_cloud_cover'], n=8)
        ds1['10m_u_wind_component'] = mpcalc.smooth_gaussian(ds1['10m_u_wind_component'], n=8)
        ds1['10m_v_wind_component'] = mpcalc.smooth_gaussian(ds1['10m_v_wind_component'], n=8)
        ds1['10m_wind_direction'] = mpcalc.smooth_gaussian(ds1['10m_wind_direction'], n=8)
        ds1['10m_wind_speed'] = mpcalc.smooth_gaussian(ds1['10m_wind_speed'], n=8)
        ds1['10m_wind_gust'] = mpcalc.smooth_gaussian(ds1['10m_wind_gust'], n=8)
        
        clear_idx_files_in_path(directory)
        
        return ds1
        
    else:
        
        clear_idx_files_in_path(directory)
    
        return ds