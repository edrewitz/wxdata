"""
This file hosts all of the functions in the WxData library that directly interact with the user. 

(C) Eric J. Drewitz 2025
"""


# Global Ensemble Forecast System (GEFS)
from wxdata.gefs.gefs import(
    
    gefs0p50,
    gefs0p50_secondary_parameters,
    gefs0p25
)

# FEMS RAWS Network
from wxdata.fems.fems import(
    get_single_station_data,
    get_raws_sig_data,
    get_nfdrs_forecast_data
)

# Real-Time Mesoscale Analysis (RTMA)
from wxdata.rtma.rtma import(
    rtma, 
    rtma_comparison
)

# NOAA 
# Storm Prediction Center Outlooks
# National Weather Service Forecasts
from wxdata.noaa.nws import get_ndfd_grids

# Observed Upper-Air Soundings
# (University of Wyoming Database)
from wxdata.soundings.wyoming_soundings import get_observed_sounding_data

# METAR Observational Data (From NOAA)
from wxdata.metars.metar_obs import download_metar_data

# WxData function using cartopy to make cyclic points
# This is for users who wish to make graphics that cross the -180/180 degree longitude line
# This is commonly used for Hemispheric graphics
from wxdata.utils.coords import cyclic_point