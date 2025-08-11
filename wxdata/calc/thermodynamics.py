"""
This file hosts functions that perform calculations using thermodynamics equations

(C) Eric J. Drewitz 2025
"""

import numpy as np

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