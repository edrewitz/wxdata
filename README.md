# WxData

![weather icon](https://github.com/edrewitz/wxdata/blob/main/icons/weather%20icon.jpg) ![python icon](https://github.com/edrewitz/wxdata/blob/main/icons/python%20logo.png)

An open-source package that helps meteorologists and weather enthusiats download, pre-process and post-process various types of weather data. 

This package only retrieves open-source weather data (i.e. nothing behind a paywall or a login). 

This package provides the following extra functionality compared to existing packages for downloading weather data:

1) Friendly for users working on VPN/PROXY connections.
   - Users input their PROXY IP address as a dictionary and pass it into the function to avoid SSL errors
     - If the user is on a VPN/PROXY Connection the following is needed:
       
                         proxies=None ---> proxies={
                                           'http':'http://url',
                                           'https':'https://url'
                                           }

                        [e.g. get_observed_sounding_data('nkx', proxies=proxies)]

   - Some data access functions work on VPN/PROXY connections without needing to define VPN/PROXY settings:
      - METARs
      - NOAA Storm Prediction Center/National Weather Service Products
      - FEMS

   - Data access methods that users need to define VPN/PROXY IP addresses if using a VPN/PROXY connection:
      - Various Forecast Models
      - Observed Sounding Data from University of Wyoming
      - Real-Time Mesoscale Analysis 
       
2) Converts GRIB variable keys into variable keys that are in plain language.
    - (e.g. 'r2' ---> '2m_relative_humidity')
      
3) Has a scanner that checks if the data files on your PC are up to date with those on the data server.
   - This is a safeguard to protect newer developers from getting temporary IP address bans from the various data servers.
   - Improves performance by preventing the potential of repetative downloading the same dataset.

4) Preserves system memory via the following methods:
   - Clears out old data files before each new data download.
   - Optional setting `clear_recycle_bin=True` in all functions.
        - When `clear_recycle_bin=True` the computer's recycle/trash bin is cleared with each run of the script using any WxData function.
        - If a user wishes to not clear out their recycle bin `set clear_recycle_bin=False`.

**WxData Module Documentation**

***Global Ensemble Forecast System (GEFS)***
1. [GEFS0P50](https://github.com/edrewitz/wxdata/blob/main/Documentation/GEFS0P50.md#global-ensemble-forecast-system-050-x-050-degree-gefs0p50)
2. [GEFS0P50 SECONDARY PARAMETERS](https://github.com/edrewitz/wxdata/blob/main/Documentation/GEFS0P50%20Secondary%20Parameters.md#global-ensemble-forecast-system-050-x-050-degree-secondary-parameters-gefs0p50-secondary-parameters)
3. [GEFS0P25](https://github.com/edrewitz/wxdata/blob/main/Documentation/GEFS0P25.md#global-ensemble-forecast-system-025-x-025-degree-gefs0p25)

         from wxdata.gefs.gefs import(
             
             gefs0p50,
             gefs0p50_secondary_parameters,
             gefs0p25
         )
   
***Real-Time Mesoscale Analysis (RTMA)***
1. [RTMA](https://github.com/edrewitz/wxdata/blob/main/Documentation/rtma.md#real-time-mesoscale-analysis-rtma)
2. [RTMA Comparison](https://github.com/edrewitz/wxdata/blob/main/Documentation/rtma%20comparison.md#real-time-mesoscale-analysis-rtma-24-hour-comparison)

         from wxdata.rtma.rtma import(
             rtma, 
             rtma_comparison
         )

***NOAA Storm Prediction Center Outlooks And National Weather Service Forecasts***
1. [Get NDFD Grids](https://github.com/edrewitz/wxdata/blob/main/Documentation/noaa.md#noaa-get-storm-prediction-center-outlooks-and-national-weather-service-forecasts-ndfd-grids)

         from wxdata.noaa.nws import get_ndfd_grids

***METAR Observations***
1. [METAR Observations](https://github.com/edrewitz/wxdata/blob/main/Documentation/metars.md#metar-observations)

         from wxdata.metars.metar_obs import download_metar_data

***FEMS RAWS Network***
1. [Get Single Station RAWS Data](https://github.com/edrewitz/wxdata/blob/main/Documentation/single_raws.md#fems-get-single-raws-station-data)
2. [Get Each SIG of RAWS Data for a Geographic Area Coordination Center](https://github.com/edrewitz/wxdata/blob/main/Documentation/raws%20sig.md#fems-get-raws-sig-data-for-a-geographic-area-coordination-center-region)
3. [Get NFDRS Forecast Data for Each SIG for a Geographic Area Coordination Center](https://github.com/edrewitz/wxdata/blob/main/Documentation/nfdrs%20forecast.md#fems-get-nfdrs-forecast-data-for-a-raws-sig-for-a-geographic-area-coordination-center-region)

         from wxdata.fems.fems import(
             get_single_station_data,
             get_raws_sig_data,
             get_nfdrs_forecast_data
         )

***Observed Atmospheric Soundings***
1. [University Of Wyoming Soundings](https://github.com/edrewitz/wxdata/blob/main/Documentation/wyoming_soundings.md)

         from wxdata.soundings.wyoming_soundings import get_observed_sounding_data

***Cyclic Points For Hemispheric Plots***
1. [Cyclic Points](https://github.com/edrewitz/wxdata/blob/main/Documentation/cyclic_point.md#using-wxdata-to-add-cyclic-points-for-hemispheric-plots)

         from wxdata.utils.coords import cyclic_point

### Citations

**MetPy**: May, R. M., Goebbert, K. H., Thielen, J. E., Leeman, J. R., Camron, M. D., Bruick, Z.,
    Bruning, E. C., Manser, R. P., Arms, S. C., and Marsh, P. T., 2022: MetPy: A
    Meteorological Python Library for Data Analysis and Visualization. Bull. Amer. Meteor.
    Soc., 103, E2273-E2284, https://doi.org/10.1175/BAMS-D-21-0125.1.

**xarray**: Hoyer, S., Hamman, J. (In revision). Xarray: N-D labeled arrays and datasets in Python. Journal of Open Research Software.

**cartopy**: Phil Elson, Elliott Sales de Andrade, Greg Lucas, Ryan May, Richard Hattersley, Ed Campbell, Andrew Dawson, Bill Little, Stephane Raynaud, scmc72, Alan D. Snow, Ruth Comer, Kevin Donkers, Byron Blay, Peter Killick, Nat Wilson, Patrick Peglar, lgolston, lbdreyer, … Chris Havlin. (2023). SciTools/cartopy: v0.22.0 (v0.22.0). Zenodo. https://doi.org/10.5281/zenodo.8216315

**NumPy**: Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). DOI: 10.1038/s41586-020-2649-2. (Publisher link).

**Pandas**: Pandas: McKinney, W., & others. (2010). Data structures for statistical computing in python. In Proceedings of the 9th Python in Science Conference (Vol. 445, pp. 51–56).

**dask**: Dask Development Team (2016). Dask: Library for dynamic task scheduling. URL http://dask.pydata.org


