"""
This file hosts functions that are additional tools when working with GRIB data.

These functions are useful for users who wish to extract the following:

1) Individual points (Plotting Model Soundings)

2) Data points along a line connecting points A and B (Plotting Model Cross-Sections)

(C) Eric J. Drewitz 2025
"""

import urllib.request
import pandas as pd
import xarray as xr
import os

from metpy.interpolate import cross_section

def station_coords(station_id):
    
    """
    This function will retrieve the latitude/longitude point for an ASOS Station ID.
    
    Required Arguments: 
    
    1) station_id (String) - The 4 letter ASOS station ID.
    
    Optional Arguments: None
    
    Returns
    -------
    
    The latitude (float) and longitude (float) of the ASOS station.    
    """
    
    if os.path.exists(f"Airport Codes"):
        pass
    else:
        os.mkdir(f"Airport Codes")
        
    if os.path.exists(f"Airport Codes/airport-codes.csv"):
        pass
    else:
        urllib.request.urlretrieve(f"https://raw.githubusercontent.com/Unidata/MetPy/refs/heads/main/staticdata/airport-codes.csv", f"Airport Codes/airport-codes.csv")
        
    df = pd.read_csv(f"Airport Codes/airport-codes.csv")
    
    df = df[(df['type'] == 'large_airport') | (df['type'] == 'medium_airport') | (df['type'] == 'small_airport')]

    df = df[df['ident'] == station_id]

    longitude = df['longitude_deg']
    latitude = df['latitude_deg']

    longitude = longitude.iloc[0]
    latitude = latitude.iloc[0]
    
    return longitude, latitude  


def pixel_query(ds, 
                latitude=None, 
                longitude=None,
                station_id=None,
                coord_names=['latitude',
                            'longitude']):
    
    """
    This function queries for the nearest pixel to a user specified point of (latitude/longitude). 
    
    This function is useful for people interested in a point forecast.
    
    Applications include
    ---------------------
    
    1) forecast soundings
    
    2) forecast meteograms
    
    3) forecast time cross-sections
    
    Required Arguments:
    
    1) ds (xarray.array) - The forecast model dataset in GRIB format. 
    
    Optional Arguments:
    
    1) station_id (String) - Default=None. The 4 letter station ID of an ASOS station.
    
    2) latitude (Float) - Default=None. The latitude of the point in decimal degrees.
    
    3) longitude (Float) - Default=None. The longitude of the point in decimal degrees.
    
    4) coord_names (String List) - Default=['latitude', 'longitude'] A list of the coordinate names (i.e. 'longitude/latitude', 'lon'/'lat', 'easting'/'northing')
    
    Returns
    -------
    
    An xarray.array for the pixel closest to the user specified coordinates or ASOS station.    
    """
    
    ds = ds.metpy.parse_cf()
    
    if station_id == None:
        
        if coord_names[0] == 'latitude' and coord_names[1] == 'longitude':
            ds = ds.sel(longitude=longitude, latitude=latitude, method='nearest')
        elif coord_names[0] == 'lat' and coord_names[1] == 'lon':
            ds = ds.sel(lon=longitude, lat=latitude, method='nearest')
        else:
            ds = ds.sel(easting=longitude, northing=latitude, method='nearest')

    else:
        
        longitude, latitude = station_coords(station_id)
        
        if coord_names[0] == 'latitude' and coord_names[1] == 'longitude':
            ds = ds.sel(longitude=longitude, latitude=latitude, method='nearest')
        elif coord_names[0] == 'lat' and coord_names[1] == 'lon':
            ds = ds.sel(lon=longitude, lat=latitude, method='nearest')
        else:
            ds = ds.sel(easting=longitude, northing=latitude, method='nearest')
            
    return ds       


def line_query(ds, 
               starting_point,
               ending_point,
               coord_names=['latitude',
                            'longitude'],
               surface_pressure_key='surface_pressure',
               north_to_south=False,
               pressure_level_key='isobaricInhPa'):
    
    """
    This function is to query for a line that connects a starting_point (A) with an ending_point (B)
    
    Applications Include
    --------------------
    
    1) Forecast cross-sections between two different geographical points.
    
    Required Arguments:
    
    1) ds (xarray.array) - The forecast model dataset in GRIB format.
    
    2) starting_point (String or Tuple) - The starting point of the line.
    
       The user has two options, either enter an ASOS station identifier as a string OR custom (lat, lon) in decimal degrees as a tuple. 
 
    3) ending_point (String or Tuple) - The ending point of the line.
    
       The user has two options, either enter an ASOS station identifier as a string OR custom (lat, lon) in decimal degrees as a tuple.    
       
    Optional Arguments:
    
    1) coord_names (String List) - Default=['latitude', 'longitude'] A list of the coordinate names (i.e. 'longitude/latitude', 'lon'/'lat', 'easting'/'northing')
    
    2) surface_pressure_key (String) - Default='surface_pressure'. The variable key for surface pressure. 
    
    3) north_to_south (Boolean) - Default=False. When set to False, lines will better reflect a more E to W oriented cross section.
       When True, lines will better reflect a more N to S oriented cross section.
       
    4) pressure_level_key (String) - Default='isobaricInhPa'. The key for the pressure level. 
    
    
    Returns
    -------
    
    5 xarray.array data arrays of pixels along a line between points A and B.
    
    1) ds_grid - The gridded variables. 
    
    2) pressure - The array of pressure levels.
    
    3) index - The indexed point number for each point along the line.
    
    4) lon - Array of longitude.
    
    5) height - Array of height levels.      
    """
    
    ds = ds.metpy.parse_cf()
    sfc_pressure = (ds[surface_pressure_key][:]) / 100
    
    if north_to_south == False:
        ref = coord_names[1]
    else:
        ref = coord_names[0]
    
    if type(starting_point) == str and type(ending_point) == str:
        
        longitude_1, latitude_1 = station_coords(starting_point)
        longitude_2, latitude_2 = station_coords(ending_point)
        
        coords_1 = (latitude_1, longitude_1)
        coords_2 = (latitude_2, longitude_2)
        
        cross = cross_section(ds, coords_1, coords_2)
        height_cross = cross_section(sfc_pressure, coords_1, coords_2)
        ds_grid, pressure, index, lon, height = xr.broadcast(cross, cross[pressure_level_key], cross['index'], cross[ref], height_cross) 
        
    else:
        cross = cross_section(ds, starting_point, ending_point)
        height_cross = cross_section(sfc_pressure, starting_point, ending_point)
        ds_grid, pressure, index, lon, height = xr.broadcast(cross, cross[pressure_level_key], cross['index'], cross[ref], height_cross) 
        
    return ds_grid, pressure, index, lon, height