from wxdata.gfs.gefs import gefs_0p50_secondary_parameters
                                      
ds = gefs_0p50_secondary_parameters('mean', 'heightAboveGround', western_bound=-120, eastern_bound=-60, northern_bound=50, southern_bound=20)

for step in range(0, len(ds['step']), 1):
    print(ds['r2'][1, step, :, :])