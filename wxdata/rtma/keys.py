"""
This file hosts dictionary functions that return values based on keys.

(C) Eric J. Drewitz 2025
"""

def rtma_files_index(model):
    
    """
    This function returns the string-index of the model run times in the RTMA files
    """
    model = model.upper()
    
    times = {
        
        'RTMA':[9, 10],
        'AK RTMA':[8, 9],
        'GU RTMA':[8, 9],
        'HI RTMA':[8, 9],
        'PR RTMA':[8, 9]
    }
    
    return times[model][0], times[model][1]