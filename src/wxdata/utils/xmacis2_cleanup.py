"""
This file hosts the functions that clean up the xmACIS2 Pandas.DataFrame to make the data easier to work with. 

(C) Eric J. Drewitz 2025
"""

import pandas as pd
import numpy as np

def missing_to_nan(df):
    
    """
    This function does replaces the missing value character 'M' with np.nan (NaN)
    
    Required Arguments:
    
    1) df (Pandas.DataFrame) - The Pandas.DataFrame of xmACIS2 data.
    
    Optional Arguments: None
    
    Returns
    -------
    
    A Pandas.DataFrame where M is replaced with NaN.
    """
    
    try:
        df = df.replace({'M':np.NaN})
    except Exception as e:
        df = df.infer_objects(copy=False)
        df.replace('M', np.nan, inplace=True)

    return df

def clean_pandas_dataframe(df):
    
    """
    This function cleans up the Pandas.DataFrame of the xmACIS2 Data.
    The ingested dataframe has each value as a string - the problem with this is we cannot perform math operations on strings.
    This function converts these strings to integers and floating points.
    
    Required Arguments:
    
    1) df (Pandas.DataFrame) - The dataframe of the xmACIS2 data.
    
    Optional Arguments: None
    
    Returns
    -------
    
    A Pandas.DataFrame with string values converted to integers and floating points.    
    """
    
    df = missing_to_nan(df)
    
    new_df = pd.DataFrame()
    
    new_df['Date'] = df['Date']
    new_df['Maximum Temperature'] = pd.to_numeric(df['Maximum Temperature'])
    new_df['Minimum Temperature'] = pd.to_numeric(df['Minimum Temperature'])
    new_df['Average Temperature'] = pd.to_numeric(df['Average Temperature'])
    new_df['Average Temperature Departure'] = pd.to_numeric(df['Average Temperature Departure'])
    new_df['Heating Degree Days'] = pd.to_numeric(df['Heating Degree Days'])
    new_df['Cooling Degree Days'] = pd.to_numeric(df['Cooling Degree Days'])
    new_df['Precipitation'] = pd.to_numeric(df['Precipitation'])
    new_df['Snowfall'] = pd.to_numeric(df['Snowfall'])
    new_df['Snow Depth'] = pd.to_numeric(df['Snow Depth'])
    new_df['Growing Degree Days'] = pd.to_numeric(df['Growing Degree Days'])
    
    return new_df