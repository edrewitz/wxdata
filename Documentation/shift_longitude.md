# Shift Longitude

***def shift_longitude(ds, 
                    lon_name='longitude'):***


    Shifts longitude values to ensure continuity across the Prime Meridian.

    Required Arguments:

    1) ds (xarray.dataarray) - The dataset of the model data.

    Optional Arguments:

    1) lon_name (String) - Default = longitude. The abbreviation for the longitude key.

    Returns
    -------

    An xarray.dataarray with longitude coordinates ranging from -180 to 180
