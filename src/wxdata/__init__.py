"""
This file hosts all of the functions in the WxData Python library that directly interact with the user. 

(C) Eric J. Drewitz 2025
"""


"""
This section of functions are for users who want full wxdata functionality.

These functions do the following:

1) Scan for the latest available data. 
    - If the data on your local machine is not up to date, new data will download automatically.
    - If the data on your local machine is up to date, new data download is bypassed.
    - This is a safeguard that prevents excessive requests on the data servers.
    
2) Builds the wxdata directory to store the weather data files. 
    - Scans for the directory branch and builds the branch if it does not exist. 

3) Downloads the data.
    - Users can define their VPN/PROXY IP Address as a (dict) in their script and pass their
      VPN/PROXY IP address into the function to avoid SSL Certificate errors when requesting data.
    - Algorithm allows for up to 5 retries with a 30 second break between each retry to resolve connection
      interruptions while not overburdening the data servers. 

4) Pre-processes the data via filename formatting and correctly filing in the wxdata directory. 

5) Post-processing by doing the following tasks:
     - Remapping GRIB2 variable keys into plain language variable keys.
     - Fixing dataset build errors and grouping all variables together.
     - Transforms longitude from 0 to 360 degrees into -180 to 180 degrees.
     - Subsetting the data to the latitude/longitude boundaries specified by the user. 
     - Converting temperature from kelvin to units the user wants (default is Celsius).
     - Returning a post-processed xarray.array to the user. 
     
6) Preserves system memory by doing the following:
     - Deleting old data files before each new download.
     - When clear_recycle_bin=True, the user's recycle bin is also cleared. 
"""

# Global Forecast System (GFS)
from wxdata.gfs.gfs import(
    gfs_0p25,
    gfs_0p25_secondary_parameters,
    gfs_0p50
)


# Global Ensemble Forecast System (GEFS)
from wxdata.gefs.gefs import(
    
    gefs_0p50,
    gefs_0p50_secondary_parameters,
    gefs_0p25
)

# European Centre for Medium-Range Weather Forecasts (ECMWF)
from wxdata.ecmwf.ecmwf import(
    ecmwf_ifs,
    ecmwf_aifs,
    ecmwf_ifs_high_res,
    ecmwf_ifs_wave
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


"""
This section hosts the utility functions accessable to the user. 

These functions provide helpful utilities when analyzing weather data. 

Utility functions are geared towards the following types of users:

1) Users who want to use their own scripts to download the data however, they
   would like to use the wxdata post-processing capabilities. 
   
2) Users who want to make hemispheric graphics or any graphics where cyclic points
   resolve missing data along the prime meridian or international dateline. 
"""
# Global Forecast System (GFS)
import wxdata.utils.gfs_post_processing as gfs_post_processing

# Global Ensemble Forecast System (GEFS)
import wxdata.utils.gefs_post_processing as gefs_post_processing

# European Centre for Medium-Range Weather Forecasts (ECMWF)
import wxdata.utils.ecmwf_post_processing as ecmwf_post_processing

# Real-Time Mesoscale Analysis (RTMA)
from wxdata.utils.rtma_post_processing import process_rtma_data


# WxData function using cartopy to make cyclic points
# This is for users who wish to make graphics that cross the -180/180 degree longitude line
# This is commonly used for Hemispheric graphics
# Function that converts the longitude dimension in an xarray.array 
# From 0 to 360 to -180 to 180
from wxdata.utils.coords import(
    cyclic_point,
    shift_longitude
)

# Functions to pixel query and query pixels along a line between points A and B
from wxdata.utils.tools import(
    pixel_query,
    line_query
)

# This is the wxdata HTTPS Client with full VPN/PROXY Support
import wxdata.client.client as client


