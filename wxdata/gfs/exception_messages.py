"""
This file hosts the functions that have exception messages for downloading GFS data.

(C) Eric J. Drewitz 2025
"""

def forecast_hour_error():
    
    print("""
          
          ERROR! User selected an hour greater than 384.
          GFS Data does not go out beyond 384 hours.        
          
          """)
    
    
def cat_error():
    
    print("""
          ERROR! User selected an invalid category. 
          
          Valid Categories
          ----------------
          
          1) atmosphere
          2) ocean
          
          Defaulting to atmosphere...         
          
          """)