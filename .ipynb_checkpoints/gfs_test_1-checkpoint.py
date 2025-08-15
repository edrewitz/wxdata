from wxdata.gfs.gefs import gefs_0p50
                                      
ds = gefs_0p50('mean', 'heightAboveGround', western_bound=-120, eastern_bound=-60, northern_bound=50, southern_bound=20)

print(ds['r2'])