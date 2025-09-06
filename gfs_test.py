from wxdata.gfs.gefs import gefs_0p50
import numpy as np
                                      
ds = gefs_0p50('mean', western_bound=-120, eastern_bound=-60, northern_bound=50, southern_bound=20, final_forecast_hour=120)

print(ds)
