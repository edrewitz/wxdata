import xarray as xr
import urllib.request
import os
import sys
import logging
import glob

try:
    os.remove(f"20250903120000-0h-enfo-pf.grib2")
except Exception as e:
    pass
urllib.request.urlretrieve(f"https://data.ecmwf.int/forecasts/20250903/12z/aifs-ens/0p25/enfo/20250903120000-0h-enfo-pf.grib2", f"20250903120000-0h-enfo-pf.grib2")

ds = xr.open_dataset(f"20250903120000-0h-enfo-pf.grib2", engine='cfgrib', filter_by_keys={'typeOfLevel': 'isobaricInhPa'})

print(ds)