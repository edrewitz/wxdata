import xarray as xr
import sys
import logging
import warnings
warnings.filterwarnings('ignore')

from wxdata.utils.file_funcs import file_paths_for_xarray
from wxdata.utils.coords import(
    shift_longitude,
    convert_lon
)

sys.tracebacklimit = 0
logging.disable()


def aigfs_post_processing(path,
                            western_bound,
                            eastern_bound,
                            northern_bound,
                            southern_bound):
    
    """
    This function post-processes the AIGFS Data into a more user-friendly format.
    
    Required Arguments:
    
    1) path (String) - The path to the AIGFS Data files.
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray.array in a plain language variable key format.     
    
    Pressure-Level Plain Language Variable Keys
    -------------------------------------------
    
    'geopotential_height'
    'specific_humidity'
    'air_temperature'
    'u_wind_component'
    'v_wind_component'
    'vertical_velocity'
    
    Surface-Level Plain Language Variable Keys
    ------------------------------------------
    
    '10m_u_wind_component'
    '10m_v_wind_component'
    'mslp'
    '2m_temperature'
    """
    
    western_bound, eastern_bound = convert_lon(western_bound, 
                                                    eastern_bound) 
    
    path = file_paths_for_xarray(path)
    
    try:
        ds = xr.open_mfdataset(path, 
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False, 
                                backend_kwargs={"indexpath": ""}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                            latitude=slice(northern_bound, southern_bound, 1))
        ds = shift_longitude(ds)
        
        try:
            ds['10m_u_wind_component'] = ds['u10']
            ds = ds.drop_vars('u10')
        except Exception as e:
            pass
        
        try:
            ds['geopotential_height'] = ds['gh']
            ds = ds.drop_vars('gh')
        except Exception as e:
            pass
        
        try:
            ds['specific_humidity'] = ds['q']
            ds = ds.drop_vars('q')
        except Exception as e:
            pass
        
        try:
            ds['air_temperature'] = ds['t']
            ds = ds.drop_vars('t')
        except Exception as e:
            pass
        
        try:
            ds['u_wind_component'] = ds['u']
            ds = ds.drop_vars('u')
        except Exception as e:
            pass
        
        try:
            ds['v_wind_component'] = ds['v']
            ds = ds.drop_vars('v')
        except Exception as e:
            pass
            
        try:
            ds['vertical_velocity'] = ds['w']
            ds = ds.drop_vars('w')
        except Exception as e:
            pass
        
        try:
            ds['total_precipitation'] = ds['tp']
            ds = ds.drop_vars('tp')
        except Exception as e:
            pass
        
        try:
            ds['10m_u_wind_component'] = ds['u10']
            ds = ds.drop_vars('u10')
        except Exception as e:
            pass
        
        try:
            ds['10m_v_wind_component'] = ds['v10']
            ds = ds.drop_vars('v10')
        except Exception as e:
            pass
            
        try:
            ds['mslp'] = ds['prmsl']
            ds = ds.drop_vars('prmsl')
        except Exception as e:
            pass
        
    except Exception as e:
        pass
    
    try:
        ds1 = xr.open_mfdataset(path, 
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False, 
                                filter_by_keys={'paramId':167},
                                backend_kwargs={"indexpath": ""}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                            latitude=slice(northern_bound, southern_bound, 1))
        ds1 = shift_longitude(ds1)
        
        try:
            ds['2m_temperature'] = ds1['t2m']
        except Exception as e:
            pass
        
    except Exception as e:
        pass
    
    ds = ds.sortby('step')
    return ds