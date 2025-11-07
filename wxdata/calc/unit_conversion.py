"""
This file hosts the functions that convert units

(C) Eric J. Drewitz
"""

def convert_temperature_units(ds, 
                              convert_to,
                              cat='mean'):
    
    """
    This function converts temperature variables from Kelvin to Fahrenheit
    
    Required Arguments: 
    
    1) ds (xarray.array) - The xarray data array 
    
    2) convert_to (String) - Convert to Celsius or Fahrenheit
    
    Optional Arguments: None
    
    Returns
    -------
    
    Temperature variables in Fahrenheit or Celsius  
    """
    convert_to = convert_to.lower()
    cat = cat.lower()
    
    params = list(ds.data_vars.keys())
    
    keyword1 = 'temperature'
    keyword2 = 'dew_point'
    keyword3 = 'dew_point_depression'
    for param in params:
        if keyword1 in param:
            if convert_to == 'celsius':
                if cat != 'spread':
                    ds[param] = ds[param] - 273.15
                else:
                    ds[param] = ds[param]
            else:
                if cat != 'spread':
                    frac = 9/5
                    ds[param] = ds[param] - 273.15
                    ds[param] = (ds[param] * frac) + 32
                else:
                    ds[param] = ds[param] * 1.8
        if keyword2 in param:
            if convert_to == 'celsius':
                if cat != 'spread':
                    ds[param] = ds[param] - 273.15
                else:
                    ds[param] = ds[param]
            else:
                if cat != 'spread':
                    frac = 9/5
                    ds[param] = ds[param] - 273.15
                    ds[param] = (ds[param] * frac) + 32
                else:
                    ds[param] = ds[param] * 1.8              
            
    return ds