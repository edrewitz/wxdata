"""
This file hosts dictionary functions that return values based on keys.

(C) Eric J. Drewitz 2025
"""

def get_run_by_keyword(url):
    
    """
    This function returns the RTMA runtime by keywords in the filename
    
    Required Arguments:
    
    1) url (String) - The download URL.
    
    Optional Arguments: None
    
    Returns
    -------
    
    The RTMA run time.     
    """
    
    keywords = []
    for i in range(0, 24, 1):
        if i < 10:
            keyword = f"t0{i}z"
        else:
            keyword = f"t{i}z"
            
        keywords.append(keyword)
        
    for key in keywords:
        if key in url:
            run = f"{key[1]}{key[2]}"
            
            return run
    

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