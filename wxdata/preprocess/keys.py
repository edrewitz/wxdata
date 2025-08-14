"""
This file hosts the function that returns a list of variable keys for a model

(C) Eric J. Drewitz 2025
"""

def get_var_keys(model):
    
    """
    This function returns a list of variable keys for a given model.

    Required Arguments:

    1) model (String) - The forecast model. 

    Optional Arguments: None

    Returns
    -------

    A list of variable keys needed for pre-processing. 
    """

    
    model = model.upper()
    
    keys = {
        'GEFS0P50':['surface', 'meanSea', 'depthBelowLandLayer', 'heightAboveGround', 'atmosphereSingleLayer', 'pressureFromGroundLayer', 'isobaricInhPa']
    }
    
    short_names = {
        
        'GEFS0P50':['t', 'r', 'u', 'v']
    }

    return keys[model], short_names[model]