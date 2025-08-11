from wxdata.gfs.gefs import gefs_0p50
                                      
ds = gefs_0p50('all members', 'heightAboveGround', western_bound=-100, eastern_bound=179, northern_bound=90, southern_bound=-90)

print(ds)