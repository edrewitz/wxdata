"""
This file hosts functions that check filenames and extract necessary data from filenames. 

(C) Eric J. Drewitz 2025
"""

def file_extension(fname):

    """
    Scans for file extension.
    """

    if fname[-4] == 'f':
        ftype = False
    else:
        ftype = True

    return ftype

def file_fhour_checker(model, fname, max_fcst_hour):

    """
    This function returns the string-index of the model run times in a file

    1) model (String) - The forecast model

    Optional Arguments: None

    Returns
    -------

    The index values of the run times in the file. 
    """
    
    hr = int(f"{fname[-9]}{fname[-8]}{fname[-7]}")

    if hr == max_fcst_hour:
        download = False
    else:
        download = True

    return download