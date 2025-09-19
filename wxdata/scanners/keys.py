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
        
def url_index(model, directory):

    """
    This function returns the string-index of the model run times in a file

    1) model (String) - The forecast model

    2) directory (String) - The directory the user wants to scan

    Optional Arguments: None

    Returns
    -------

    The index values of the run times in the file. 
    """
    
    if directory == 'atmos':
    
        times = {
            'GEFS0P25':[-19, -18],
            'GEFS0P50':[-18, -17],
            'GEFS0P50 SECONDARY PARAMETERS':[-18, -17],
            'GFS0P25':[-9, -8],
            'GFS0P25 SECONDARY PARAMETERS':[-9, -8]
        }
        
    elif directory == 'chem':

        times = {
            'GEFS0P25':[-18, -17],
            'GEFS0P50':[-17, -16],
            'GEFS0P50 SECONDARY PARAMETERS':[-18, -17],
            'GFS0P25':[-9, -8],
            'GFS0P25 SECONDARY PARAMETERS':[-9, -8]
        }
        
    else:
        
        times = {
            'GEFS0P25':[-16, -15],
            'GEFS0P50':[-16, -15],
            'GEFS0P50 SECONDARY PARAMETERS':[-16, -15],
            'GFS0P25':[-9, -8],
            'GFS0P25 SECONDARY PARAMETERS':[-9, -8]
        }        
        

    return times[model][0], times[model][1]


def index(model, directory):

    """
    This function returns the string-index of the model run times in a file

    1) model (String) - The forecast model

    Optional Arguments: None

    Returns
    -------

    The index values of the run times in the file. 
    """
    directory = directory.upper()
    
    if directory == 'ATMOS':
    
        times = {
            'GEFS0P25':[7, 8],
            'GEFS0P50':[7, 8],
            'GEFS0P50 SECONDARY PARAMETERS':[7, 8],
            'GFS0P25':[5, 6],
            'GFS0P25 SECONDARY PARAMETERS':[5, 6]
        }
        
    elif directory == 'CHEM':
        
        times = {
            'GEFS0P25':[7, 8],
            'GEFS0P50':[11, 12],
            'GFS0P25':[5, 6],
            'GFS0P25 SECONDARY PARAMETERS':[5, 6]
        }
    else:
        
        times = {
            'GEFS0P25':[11, 12],
            'GFS0P25':[5, 6],
            'GFS0P25 SECONDARY PARAMETERS':[5, 6]
        }

    return times[model][0], times[model][1]