"""
This file hosts the functions that will calculate derived model fields.

These calculations will occur after the post-processing. 

(C) Eric J. Drewitz
"""

import xarray as xr
import metpy.calc as mpcalc

from metpy.units import units


def rtma_derived_fields(ds,
                        convert_temperature,
                        convert_to):
    
    try:
        if convert_temperature == True:
            if convert_to == 'celsius':
                unit = 'degC'
            else:
                unit = 'degF'
        else:
            unit = 'kelvin'
    except Exception as e:
        pass
    
    try:
        ds['2m_apparent_temperature'] = mpcalc.apparent_temperature(ds['2m_temperature'] * units(unit), ds['2m_relative_humidity'], ds['10m_wind_speed'] * units('m/s'))
    except Exception as e:
        pass
    
    
    ds = ds.metpy.dequantify()
    
    try:
        ds['2m_dew_point_depression'] = ds['2m_temperature'] - ds['2m_dew_point']
    except Exception as e:
        pass
        
    return ds

