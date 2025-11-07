"""
This file hosts the functions the user interacts with to download GFS data. 

(C) Eric J. Drewitz 2025
"""

import urllib.request
import sys
import os
import warnings
import time
import wxdata.utils.gefs_post_processing as gefs_post_processing
warnings.filterwarnings('ignore')

from wxdata.gefs.file_funcs import(
    
    build_directory,
    clear_idx_files,
    clear_empty_files
    
)
from wxdata.gefs.url_scanners import(
    
    gefs_0p50_url_scanner,
    gefs_0p50_secondary_parameters_url_scanner,
    gefs_0p25_url_scanner
)

from wxdata.gefs.process import(
    
    process_gefs_data,
    process_gefs_secondary_parameters_data
    
)

from wxdata.utils.file_funcs import(
     custom_branch,
     custom_branches,
     clear_gefs_idx_files
)

from wxdata.calc.derived_fields import gefs_primary_derived_fields
from wxdata.calc.unit_conversion import convert_temperature_units
from wxdata.utils.file_scanner import local_file_scanner
from wxdata.utils.recycle_bin import *


def gfs_0p25(cat, 
            final_forecast_hour, 
            western_bound, 
            eastern_bound, 
            northern_bound, 
            southern_bound, 
            proxies, 
            step, 
            variables
            custom_directory='default',
            clear_recycle_bin=True):
    
    """
    This function downloads GFS data and saves it to a folder. 
    
    
    """