# Using WxData To Add Cyclic Points For Hemispheric Plots

***def cyclic_point(ds, 
                 parameter, 
                 lon_name='longitude'):***

This function returns a data array for the full 360 degree Earth. 

Required Arguments:

1) ds (xarray data array) - The xarray dataset.

2) parameter (String) - The parameter or variable the user is plotting. 

Optional Arguments:

1) lon_name (String) - The name of the longitude variable. Usually is lon or longitude. 

Returns
-------

An xarray data array that interpolates along 180 degrees longitude.   
