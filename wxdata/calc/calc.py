import numpy as np

def fahrenheit_to_celsius(f):
    frac = 5/9
    c = frac * (f - 32)
    return c

def fahrenheit_to_kelvin(f):
    frac = 5/9
    c = frac * (f - 32)
    return c + 273.15

def celsius_to_fahrenheit(c):
    frac = 9/5
    f = (c * frac) + 32
    return f

def kelvin_to_fahrenheit(k):
    c = k - 273.15
    frac = 9/5
    f = (c * frac) + 32
    return f    

def get_u_and_v(wind_speed, wind_dir):

    """
    This function calculates the u and u wind components

    Required Arguments:

    1) wind_speed (Float or Integer) 

    2) wind_direction (Float or Integer)

    Returns
    -------

    u and v wind components
    """

    u = wind_speed * np.cos(wind_dir)
    v = wind_speed * np.sin(wind_dir)

    return u, v

def saturation_vapor_pressure(temperature):

    """
    This function calculates the saturation vapor pressure from temperature.
    This function uses the formula from Bolton 1980.   

    Required Arguments:

    1) temperature (Float or Integer)

    Returns
    -------

    The saturation vapor pressure
    """

    e = 6.112 * np.exp(17.67 * (temperature) / (temperature + 243.5))
    return e


def relative_humidity(temperature, dewpoint):

    """
    This function calculates the relative humidity from temperature and dewpoint. 

    Required Arguments:

    1) temperature (Float or Integer)

    2) dewpoint (Float or Integer)

    Returns
    -------

    The relative humidity
    """

    e = saturation_vapor_pressure(dewpoint)
    e_s = saturation_vapor_pressure(temperature)
    return (e / e_s) * 100


def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def exponent(a, b):
    return a ** b

    
