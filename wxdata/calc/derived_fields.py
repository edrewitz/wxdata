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

def gefs_primary_derived_fields(ds, 
                        convert_temperature,
                        convert_to):
    
    """
    This function calculates the derived fields from the standard GEFS Primary fields. 
    
    Required Arguments:
    
    1) ds (xarray.array) - The xarray.array GEFS dataset. 
    
    2) convert_temperature (Boolean) - Default=True. When set to True, Temperature and Dew Point data is converted from Kelvin to either Celsius or Fahrenheit.
        When set to False, the data remains in Kelvin.
        
    3) convert_to (String) - Default='celsius'. When convert_temperature is set to True, we need to specify the new temperature units. This can be done by
        convert_to='celsius' (default) or convert_to='fahrenheit'.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray.array with the additional derived fields.     
    """
    
    ds = ds
    
    if convert_temperature == True:
        if convert_to == 'celsius':
            unit = 'degC'
        else:
            unit = 'degF'
    else:
        unit = 'kelvin'
        
    try:
        ds['2m_dew_point'] = mpcalc.dewpoint_from_relative_humidity(ds['2m_temperature'] * units(unit), ds['2m_relative_humidity'])
    except Exception as e:
        pass
    
    try:
        ds_list = []
        for i in range(0, len(ds['number']), 1):
            ds['2m_dew_point'] = mpcalc.dewpoint_from_relative_humidity(ds['2m_temperature'][i, :, :, :] * units(unit), ds['2m_relative_humidity'][i, :, :, :])
            ds_list.append(ds['2m_dew_point'])
        ds1 = xr.concat(ds_list, dim='number')
        ds['2m_dew_point'] = ds1
    except Exception as e:
        pass    

    try:
        ds['dew_point'] = mpcalc.dewpoint_from_relative_humidity(ds['air_temperature'] * units(unit), ds['relative_humidity'])
    except Exception as e:
        pass
    
    try:
        ds_list = []
        for i in range(0, len(ds['number']), 1):
            ds['dew_point'] = mpcalc.dewpoint_from_relative_humidity(ds['air_temperature'][i, :, :, :] * units(unit), ds['relative_humidity'][i, :, :, :])
            ds_list.append(ds['dew_point'])
        ds1 = xr.concat(ds_list, dim='number')
        ds['dew_point'] = ds1
    except Exception as e:
        pass    
    
    try:
        ds['potential_temperature'] = mpcalc.potential_temperature(ds['isobaricInhPa'] * units('hPa'), ds['air_temperature'] * units(unit))
    except Exception as e:
        pass
    
    try:
        ds_list = []
        for i in range(0, len(ds['number']), 1):
            ds['potential_temperature'] = mpcalc.potential_temperature(ds['isobaricInhPa'] * units('hPa'), ds['air_temperature'][i, :, :, :] * units(unit))
            ds_list.append(ds['potential_temperature'])
        ds1 = xr.concat(ds_list, dim='number')
        ds['potential_temperature'] = ds1
    except Exception as e:
        pass     
    
    try:
        if convert_temperature == True:
            ds['potential_temperature'] = ds['potential_tempetature'].to(units.kelvin)
        else:
            pass
    except Exception as e:
        pass
    
    try:
        ds['wind_direction'] = mpcalc.wind_direction(ds['u_wind_component'] * units('m/s'), ds['v_wind_component'] * units('m/s'))
    except Exception as e:
        pass
    
    try:
        ds_list = []
        for i in range(0, len(ds['number']), 1):
            ds['wind_direction'] = mpcalc.wind_direction(ds['u_wind_component'][i, :, :, :] * units('m/s'), ds['v_wind_component'][i, :, :, :] * units('m/s'))
            ds_list.append(ds['wind_direction'])
        ds1 = xr.concat(ds_list, dim='number')
        ds['wind_direction'] = ds1
    except Exception as e:
        pass         
    
    ds = ds.metpy.dequantify()    
    
    try:
        ds['2m_dew_point_depression'] = ds['2m_temperature'] - ds['2m_dew_point']
    except Exception as e:
        pass
    
    try:
        ds_list = []
        for i in range(0, len(ds['number']), 1):
            ds['2m_dew_point_depression'] = ds['2m_temperature'][i, :, :, :] - ds['2m_dew_point'][i, :, :, :]
            ds_list.append(ds['2m_dew_point_depression'])
        ds1 = xr.concat(ds_list, dim='number')
        ds['2m_dew_point_depression'] = ds1
    except Exception as e:
        pass
     
    
    try:
        ds['dew_point_depression'] = ds['air_temperature'] - ds['dew_point']
    except Exception as e:
        pass
    
    try:
        ds_list = []
        for i in range(0, len(ds['number']), 1):
            ds['dew_point_depression'] = ds['air_temperature'][i, :, :, :] - ds['dew_point'][i, :, :, :]
            ds_list.append(ds['dew_point_depression'])
        ds1 = xr.concat(ds_list, dim='number')
        ds['dew_point_depression'] = ds1
    except Exception as e:
        pass
    
    return ds


def derived_ecmwf_ifs_fields(ds,
                             convert_temperature,
                             convert_to):
    
    
    ds = ds
    
    if convert_temperature == True:
        if convert_to == 'celsius':
            unit = 'degC'
        else:
            unit = 'degF'
    else:
        unit = 'kelvin'
    
    try:
        ds['2m_dew_point_depression'] = ds['2m_temperature'] - ds['2m_dew_point']
    except Exception as e:
        pass
    
    try:
        ds['absolute_vortcity'] = mpcalc.absolute_vorticity(ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['absolute_momentum'] = mpcalc.absolute_momentum(ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['ageostrophic_wind'] = mpcalc.ageostrophic_wind(ds['geopotential_height'], ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['curvature_vorticity'] = mpcalc.curvature_vorticity(ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['divergence'] = mpcalc.divergence(ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['geostrophic_wind'] = mpcalc.geostrophic_wind(ds['geopotential_height'])
    except Exception as e:
        pass
    
    try:
        ds['dew_point'] = mpcalc.dewpoint_from_relative_humidity(ds['air_temperature'], ds['relative_humidity'])
    except Exception as e:
        pass
    
    try:
        ds['dew_point_depression'] = ds['air_temperature'] - ds['dew_point']
    except Exception as e:
        pass
    
    try:
        ds['temperature_advection'] = mpcalc.advection(ds['air_temperature'], u=ds['u_wind_component'], v=ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['vorticity_advection'] = mpcalc.advection(ds['absolute_vortcity'], u=ds['u_wind_component'], v=ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['precipitable_water_advection'] = mpcalc.advection(ds['precipitable_water'], u=ds['u_wind_component'], v=ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['humidity_advection'] = mpcalc.advection(ds['relative_humidity'], u=ds['u_wind_component'], v=ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['potential_temperature'] = mpcalc.potential_temperature(ds['isobaricInhPa'], ds['air_temperature'])
    except Exception as e:
        pass
    
    try:
        ds['frontogenesis'] = mpcalc.frontogenesis(ds['potential_temperature'], ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
    
    try:
        ds['mixing_ratio'] = mpcalc.mixing_ratio_from_relative_humidity(ds['isobaricInhPa'], ds['air_temperature'], ds['relative_humidity'])
    except Exception as e:
        pass
    
    try:
        ds['moist_lapse_rate'] = mpcalc.moist_lapse(ds['isobaricInhPa'], ds['air_temperature'])
    except Exception as e:
        pass
    
    try:
        ds['dry_lapse_rate'] = mpcalc.dry_lapse(ds['isobaricInhPa'], ds['air_temperature'])
    except Exception as e:
        pass
    
    try:
        ds['showalter_index'] = mpcalc.showalter_index(ds['isobaricInhPa'], ds['air_temperature'], ds['dew_point'])
    except Exception as e:
        pass
    
    try:
        ds['bulk_shear'] = mpcalc.bulk_shear(ds['isobaricInhPa'], ds['u_wind_component'], ds['v_wind_component'])
    except Exception as e:
        pass
        
        
    ds = ds.metpy.dequantify()
    
    return ds