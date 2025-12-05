# WxData

<img src="https://github.com/edrewitz/wxdata/blob/main/icons/weather%20icon.jpg" width="200" alt="Alt text" /> <img src="https://github.com/edrewitz/wxdata/blob/main/icons/python%20logo.png" width="200" alt="Alt text" />

[![Conda Recipe](https://img.shields.io/badge/recipe-wxdata-green.svg)](https://anaconda.org/conda-forge/wxdata) [![Conda Version](https://img.shields.io/conda/vn/conda-forge/wxdata.svg)](https://anaconda.org/conda-forge/wxdata) [![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/wxdata.svg)](https://anaconda.org/conda-forge/wxdata) ![PyPI](https://img.shields.io/pypi/v/wxdata?label=pypi%20wxdata) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/wxdata/badges/license.svg)](https://anaconda.org/conda-forge/wxdata) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/wxdata/badges/latest_release_date.svg)](https://anaconda.org/conda-forge/wxdata) 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17811303.svg)](https://doi.org/10.5281/zenodo.17811303)



Anaconda Downloads

[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/wxdata.svg)](https://anaconda.org/conda-forge/wxdata)


PIP Downloads:

![PyPI - Downloads](https://img.shields.io/pypi/dm/wxdata)



**(C) Eric J. Drewitz 2025**

An open-source package that helps meteorologists and weather enthusiats download, pre-process and post-process various types of weather data. 

This package only retrieves open-source publicly available weather data. 

This package provides the following extra functionality compared to existing packages for downloading weather data:

**How To Install**

Copy and paste either command into your terminal or anaconda prompt:

*Install via Anaconda*

`conda install wxdata`

*Install via pip*

`pip install wxdata`

1) Friendly for users working on VPN/PROXY connections.
   - Users input their PROXY IP address as a dictionary and pass it into the function to avoid SSL errors
     - If the user is on a VPN/PROXY Connection the following is needed:
       
                         proxies=None ---> proxies={
                                           'http':'http://url',
                                           'https':'https://url'
                                           }

                        [e.g. get_observed_sounding_data('nkx', proxies=proxies)]

   For more information on configuring proxies: https://requests.readthedocs.io/en/latest/user/advanced/#proxies

   - Some data access functions work on VPN/PROXY connections without needing to define VPN/PROXY settings:
      - METARs
      - NOAA Storm Prediction Center/National Weather Service Products
      - FEMS

   - Data access methods that users need to define VPN/PROXY IP addresses if using a VPN/PROXY connection:
      - Various Forecast Models
      - Observed Sounding Data from University of Wyoming
      - Real-Time Mesoscale Analysis 
       
1) Converts GRIB variable keys into variable keys that are in plain language.
    - (e.g. 'r2' ---> '2m_relative_humidity')
      
2) Has a scanner that checks if the data files on your PC are up to date with those on the data server.
   - This is a safeguard to protect newer developers from getting temporary IP address bans from the various data servers.
   - Improves performance by preventing the potential of repetative downloading the same dataset.

3) Preserves system memory via the following methods:
   - Clears out old data files before each new data download.
   - Optional setting `clear_recycle_bin=True` in all functions.
        - When `clear_recycle_bin=True` the computer's recycle/trash bin is cleared with each run of the script using any WxData function.
        - If a user wishes to not clear out their recycle bin `set clear_recycle_bin=False`.
    
## WxData Examples

*Regular Users*
1) [Downloading METAR Data](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/metars.ipynb)
2) [Downloading Observed Sounding Data](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/soundings.ipynb)
3) [Downloading the first 72 hours of the ECMWF IFS and ECMWF AIFS](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/ecmwf.ipynb)
4) [Downloading the GEFS members p01 and p02 for only Temperature](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/gefs.ipynb)
5) [Downloading the Real-Time Mesoscale Analysis (RTMA)](https://github.com/edrewitz/WxData/blob/main/Documentation/RTMA%20Post%20Processing.md)
6) [Downloading the RAWS SIG Group Fuels Data and the NFDRS Forecast for the RAWS SIG Groups for the South Ops Geographic Area Coordination Center](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/fems.ipynb)
7) [Downloading the SPC Convective Outlook for CONUS](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/spc.ipynb)
8) [Downloading NWS Maximum Temperature Forecast for Hawaii](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/nws_hi.ipynb)
9) [Downloading the GFS0P25 then performing pixel and line queries on the data](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/GFS.ipynb)

*Advanced Users*
1) [Using the `client` module to download the latest HadCRUT5 Analysis netCDF file and open this dataset in xarray](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/hadcrut5.ipynb)
2) [Downloading the GFS0P25 for temperature fields and using run_external_scripts() to post-process this GFS0P25 dataset in an external Python script](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/external_scripts.ipynb)

## WxData Documentation

***Global Forecast System (GFS)***
1. [GFS0P25](https://github.com/edrewitz/WxData/blob/main/Documentation/GFS0P25.md)
2. [GFS0P25 SECONDARY PARAMETERS](https://github.com/edrewitz/WxData/blob/main/Documentation/GFS0P25%20Secondary%20Parameters.md)
3. [GFS0P50](https://github.com/edrewitz/WxData/blob/main/Documentation/GEFS0P50.md)

***Global Ensemble Forecast System (GEFS)***
1. [GEFS0P50](https://github.com/edrewitz/wxdata/blob/main/Documentation/GEFS0P50.md#global-ensemble-forecast-system-050-x-050-degree-gefs0p50)
2. [GEFS0P50 SECONDARY PARAMETERS](https://github.com/edrewitz/wxdata/blob/main/Documentation/GEFS0P50%20Secondary%20Parameters.md#global-ensemble-forecast-system-050-x-050-degree-secondary-parameters-gefs0p50-secondary-parameters)
3. [GEFS0P25](https://github.com/edrewitz/wxdata/blob/main/Documentation/GEFS0P25.md#global-ensemble-forecast-system-025-x-025-degree-gefs0p25)

***ECMWF Open Data***
1. [ECMWF IFS](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF_IFS.md)
2. [ECMWF AIFS](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF_AIFS.md)
3. [ECMWF High Resolution IFS](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF_High_Res_IFS.md)
4. [ECMWF IFS Wave](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF_IFS_Wave.md)
   
***Real-Time Mesoscale Analysis (RTMA)***
1. [RTMA](https://github.com/edrewitz/wxdata/blob/main/Documentation/rtma.md#real-time-mesoscale-analysis-rtma)
2. [RTMA Comparison](https://github.com/edrewitz/wxdata/blob/main/Documentation/rtma%20comparison.md#real-time-mesoscale-analysis-rtma-24-hour-comparison)

***NOAA Storm Prediction Center Outlooks And National Weather Service Forecasts***
1. [Get NDFD Grids](https://github.com/edrewitz/wxdata/blob/main/Documentation/noaa.md#noaa-get-storm-prediction-center-outlooks-and-national-weather-service-forecasts-ndfd-grids)

***METAR Observations***
1. [METAR Observations](https://github.com/edrewitz/wxdata/blob/main/Documentation/metars.md#metar-observations)

***FEMS RAWS Network***
1. [Get Single Station RAWS Data](https://github.com/edrewitz/wxdata/blob/main/Documentation/single_raws.md#fems-get-single-raws-station-data)
2. [Get Each SIG of RAWS Data for a Geographic Area Coordination Center](https://github.com/edrewitz/wxdata/blob/main/Documentation/raws%20sig.md#fems-get-raws-sig-data-for-a-geographic-area-coordination-center-region)
3. [Get NFDRS Forecast Data for Each SIG for a Geographic Area Coordination Center](https://github.com/edrewitz/wxdata/blob/main/Documentation/nfdrs%20forecast.md#fems-get-nfdrs-forecast-data-for-a-raws-sig-for-a-geographic-area-coordination-center-region)

***Observed Atmospheric Soundings***
1. [University Of Wyoming Soundings](https://github.com/edrewitz/wxdata/blob/main/Documentation/wyoming_soundings.md)

***GFS Post-Processing***
1. [Primary GFS Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/Primary%20GFS%20Post%20Processing.md)
2. [Secondary GFS Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/Secondary%20GFS%20Post%20Processing.md)

***GEFS Post-Processing***
1. [Primary GEFS Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/Primary%20GEFS%20Post-Processing.md)
2. [Secondary GEFS Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/Secondary%20GEFS%20Post%20Processing.md)

***ECMWF Post-Processing***
1. [ECMWF IFS and ECMWF High Resolution IFS](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF%20IFS%20Post%20Processing.md)
2. [ECMWF AIFS](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF%20AIFS%20Post%20Processing.md)
3. [ECMWF IFS Wave](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF%20IFS%20Wave%20Post%20Processing.md)

***Real-Time Mesoscale Analysis Post-Processing***
1. [RTMA](https://github.com/edrewitz/WxData/blob/main/Documentation/RTMA%20Post%20Processing.md)

***xmACIS2 Climate Data***
1. [xmACIS2 Client](https://github.com/edrewitz/WxData/blob/main/Documentation/xmacis2_client.md)

***Cyclic Points For Hemispheric Plots***
1. [Cyclic Points](https://github.com/edrewitz/wxdata/blob/main/Documentation/cyclic_point.md#using-wxdata-to-add-cyclic-points-for-hemispheric-plots)

***Shifting Longitude From 0 to 360 --> -180 to 180***
1. [shift_longitude](https://github.com/edrewitz/WxData/blob/main/Documentation/shift_longitude.md)

***Pixel Query***
1. [pixel_query](https://github.com/edrewitz/WxData/blob/main/Documentation/pixel_query.md)

***Line Query***
1. [line_query](https://github.com/edrewitz/WxData/blob/main/Documentation/line_query.md)

***Running External Python Scripts In Your Workflow***

1 [run_external_scripts](https://github.com/edrewitz/WxData/blob/main/Documentation/run_external_scripts.md)

## Importing Functions from WxData

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
            from wxdata import(
                gfs_0p25,
                gfs_0p25_secondary_parameters,
                gfs_0p50
            )


            # Global Ensemble Forecast System (GEFS)
            from wxdata import(
                gefs_0p50,
                gefs_0p50_secondary_parameters,
                gefs_0p25
            )

            # European Centre for Medium-Range Weather Forecasts (ECMWF)
            from wxdata import(
                ecmwf_ifs,
                ecmwf_aifs,
                ecmwf_ifs_high_res,
                ecmwf_ifs_wave
            )

            # FEMS RAWS Network
            from wxdata import(
                get_single_station_data,
                get_raws_sig_data,
                get_nfdrs_forecast_data
            )

            # Real-Time Mesoscale Analysis (RTMA)
            from wxdata import(
                rtma, 
                rtma_comparison
            )

            # NOAA 
            # Storm Prediction Center Outlooks
            # National Weather Service Forecasts
            from wxdata import get_ndfd_grids

            # Observed Upper-Air Soundings
            # (University of Wyoming Database)
            from wxdata import get_observed_sounding_data

            # METAR Observational Data (From NOAA)
            from wxdata import download_metar_data


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
            from wxdata import gfs_post_processing

            # Global Ensemble Forecast System (GEFS)
            from wxdata import gefs_post_processing

            # European Centre for Medium-Range Weather Forecasts (ECMWF)
            from wxdata import ecmwf_post_processing

            # Real-Time Mesoscale Analysis (RTMA)
            from wxdata import process_rtma_data


            # WxData function using cartopy to make cyclic points
            # This is for users who wish to make graphics that cross the -180/180 degree longitude line
            # This is commonly used for Hemispheric graphics
            # Function that converts the longitude dimension in an xarray.array 
            # From 0 to 360 to -180 to 180
            from wxdata import(
                cyclic_point,
                shift_longitude
            )

            # Functions to pixel query and query pixels along a line between points A and B
            from wxdata import(
                pixel_query,
                line_query
            )

            # These are the wxdata HTTPS Clients with full VPN/PROXY Support
            # Client List:
            #  - get_gridded_data()
            #  - get_csv_data()
            #  - get_xmacis_data()
            from wxdata import client

            # This function executes a list of Python scripts in the order the user lists them
            from wxdata import run_external_scripts



   
   


## Citations

**MetPy**: May, R. M., Goebbert, K. H., Thielen, J. E., Leeman, J. R., Camron, M. D., Bruick, Z.,
    Bruning, E. C., Manser, R. P., Arms, S. C., and Marsh, P. T., 2022: MetPy: A
    Meteorological Python Library for Data Analysis and Visualization. Bull. Amer. Meteor.
    Soc., 103, E2273-E2284, https://doi.org/10.1175/BAMS-D-21-0125.1.

**xarray**: Hoyer, S., Hamman, J. (In revision). Xarray: N-D labeled arrays and datasets in Python. Journal of Open Research Software.

**cartopy**: Phil Elson, Elliott Sales de Andrade, Greg Lucas, Ryan May, Richard Hattersley, Ed Campbell, Andrew Dawson, Bill Little, Stephane Raynaud, scmc72, Alan D. Snow, Ruth Comer, Kevin Donkers, Byron Blay, Peter Killick, Nat Wilson, Patrick Peglar, lgolston, lbdreyer, … Chris Havlin. (2023). SciTools/cartopy: v0.22.0 (v0.22.0). Zenodo. https://doi.org/10.5281/zenodo.8216315

**NumPy**: Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). DOI: 10.1038/s41586-020-2649-2. (Publisher link).

**Pandas**: Pandas: McKinney, W., & others. (2010). Data structures for statistical computing in python. In Proceedings of the 9th Python in Science Conference (Vol. 445, pp. 51–56).

**dask**: Dask Development Team (2016). Dask: Library for dynamic task scheduling. URL http://dask.pydata.org

**cfgrib**: Author: ECMWF, Year: (2025), Title: cfgrib: A Python interface to map GRIB files to xarray, Source: https://github.com/ecmwf/cfgrib 

## Data Sources

1) [National Oceanic and Atmospheric Administration/National Center for Environmental Prediction](https://nomads.ncep.noaa.gov/)
2) [European Centre for Medium-Range Weather Forecasts](https://data.ecmwf.int/forecasts/)
3) [University of Wyoming](http://www.weather.uwyo.edu/upperair/sounding.shtml)
4) [National Oceanic and Atmospheric Administration/National Weather Service](https://tgftp.nws.noaa.gov/)
5) [National Oceanic and Atmospheric Administration/Aviation Weather Center](https://aviationweather.gov/)
6) [Applied Climate Information System (ACIS)](https://www.rcc-acis.org/docs_webservices.html)


