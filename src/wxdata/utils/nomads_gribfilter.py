"""
This file hosts the functions that parse the plain language into NCEP/NOMADS GRIB Filter variable keys for the data request URL

(C) Eric J. Drewitz 2025
"""

def var_keys(varKey):
    
    """
    This function is a dictionary converting plain language variable names into GRIB Filter variable keys. 
    
    Required Arguments: 
    
    1) varKey (String) - The variable key in plain language format. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    The key for an item in the varKeys list.     
    """
    

    params = {
        'best lifted index':'4LFTX',
        '5 wave geopotential height':'5WAVH',
        'absolute vorticity':'ABSV',
        'temperature':'TMP',
        'dew point':'DPT',
        'convective precipitation':'ACPCP',
        'albedo':'ALBDO',
        'apparent temperature':'APTMP',
        'brightness temperature':'BRTMP',
        'convective available potential energy':'CAPE',
        'clear sky uv-b downward solar flux':'CDUVB',
        'convective inhibition':'CIN',
        'cloud mixing ratio':'CLWMR',
        'plant canopy surface water':'CNWAT',
        'percent frozen precipitaion':'CPOFP',
        'convective precipitation rate':'CPRAT',
        'cloud water':'CWAT',
        'cloud work function':'CWORK',
        'uv-b downward solar flux':'DUVB',
        'field capacity':'FLDCP',
        'surface friction velocity':'FRICV',
        'ground heat flux':'GFLUX',
        'wind gust':'GUST',
        'geopotential height':'HGT',
        'sunshine duration':'SUNSD',
        'haines index':'HINDEX',
        'storm relative helicity':'HLCY',
        'planetary boundary layer height':'HPBL',
        'icao standard atmosphere reference height':'ICAHT',
        'ice cover':'ICEC',
        'graupel':'GRLE',
        'ice growth rate':'ICEG',
        'icing':'ICIP',
        'high cloud cover':'HCDC',
        'middle cloud cover':'MCDC',
        'low cloud cover':'LCDC',
        'icing severity':'ICSEV',
        'land cover':'LAND',
        'surface lifted index':'LFTX',
        'montgomery stream function':'MNTSF',
        'mslp (eta model reduction)':'MSLET',
        'large scale non-convective precipitation':'NCPCP',
        'ozone mixing ratio':'O3MR',
        'potential evaporation rate':'PEVPR',
        'parcel lifted index (to 500mb)':'PLI',
        'pressure level from which parcel was lifted':'PLPL',
        'potential temperature':'POT',
        'precipitation rate':'PRATE',
        'pressure':'PRES',
        'rain mixing ratio':'RWMR',
        'potential vorticity':'PVORT',
        'precipitable water':'PWAT',
        'composite reflectivity':'REFC',
        'reflectivity':'REFD',
        'relative humidity':'RH',
        'surface roughness':'SFCR',
        'snow phase-change heat flux':'SNOHF',
        'snow cover':'SNOWC',
        'liquid volumetric soil moisture (non-frozen)':'SOILL',
        'volumetric soil moisture content':'SOILW',
        'specific humidity':'SPFH',
        'sunshine duration':'SUNSD',
        'soil type':'SOTYP',
        'total cloud cover':'TCDC',
        'total ozone':'TOZNE',
        'soil temperature':'TSOIL',
        'momentum flux (u-component)':'UFLX',
        'u-component of wind':'UGRD',
        'zonal flux of gravity wave stress':'U-GWD',
        'u-component of storm motion':'USTM',
        'upward shortwave radiation flux':'USWRF',
        'momentum flux (v-component)':'VFLX',
        'v-component of wind':'VGRD',
        'meridional flux of gravity wave stress':'V-GWD',
        'visibility':'VIS',
        'vegetation':'VEG',
        'ventilation rate':'VRATE',
        'v-component of storm motion':'VSTM',
        'vertical velocity (pressure)':'VVEL',
        'vertical velocity (height)':'DZDT',
        'vertical speed shear':'VWSH',
        'water runoff':'WATR',
        'wilting point':'WILT',
        'total precipitation':'APCP',
        'categorical freezing rain':'CFRZR',
        'categorical ice pellets':'CICEP',
        'categorical freezing rain':'CFRZR',
        'categorical rain':'CRAIN',
        'categorical snow':'CSNOW',
        'downward longwave radiation flux':'DLWRF',
        'downward shortwave radiation flux':'DSWRF',
        'ice thickness':'ICETK',
        'ice temperature':'ICETMP',
        'ice water mixing ratio':'ICMR',
        'latent heat net flux':'LHTFL',
        'mean sea level pressure':'PRMSL',
        'sensible heat net flux':'SHTFL',
        'snow mixing ratio':'SNMR',
        'snow depth':'SNOD',
        'maximum temperature':'TMAX',
        'minimum temperature':'TMIN',
        'upward longwave radiation flux':'ULWRF',
        'water equivalent of accumulated snow depth':'WEASD'
        
        
    }

    return params[varKey]

def key_list(varKeys):
    
    """
    This function creates a list of GRIB Filter Variable Keys from the Plain Language Keys. 
    
    Required Arguments: 
    
    1) varKeys (List) - A list of the variable names. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    A list of the variable keys in GRIB format. 
    """

    var_list = []
    keys = []

    for v in varKeys:
        v = v.lower()
        var_list.append(v)

    for var in var_list:
        key = var_keys(var)
        keys.append(key)
        
    return keys


def result_string(keys):
    
    """
    This function returns the variable section of the data request URL for the NOMADS GFS/GEFS data. 
    
    Required Arguments:
    
    1) keys (List) - The list of variable keys. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    The variable list in the form of a string for the URL using GRIB Filter Keys. 
    """

    result = ""
    for key in keys:
        result += "&var_" + str(key) + "=on"
        
    return result