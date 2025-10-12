"""
This file will host exception messages to alert the user when they enter something wrong. 

(C) Eric J. Drewitz 2025
"""

class gefs0p50:
    
    """
    This class will host the error message functions for the GEFS0P50
    """

    def gefs0p50_cat_error(model):
        
        model = model.upper()
        
        if model == 'GEFS0P50':

            print(f"""
                    Error! User entered an invalid category. Here are the acceptable categories
                    
                        Valid categories
                        -----------------
            
                            1) mean
                            2) members
                            3) spread
                            4) control
                            
                            
                    Defaulting to 'mean' for now.   
                
                """)
            
        else:
            print(f"""
                    Error! User entered an invalid category. Here are the acceptable categories
                    
                        Valid categories
                        -----------------
            
                            1) control
                            2) members
                                                        
                            
                    Defaulting to 'control' for now.   
                
                """)            
        
    def forecast_hour_error():
        
        print(f"""
                Error! User entered a forecast hour > 384. 
                
                Defaulting to 384 as the final_forecast_hour. 
              """)
        
class gefs0p25:

    """
    This class will host the error message functions for the GEFS0P25
    """
    
    def gefs0p25_cat_error():
        
        print(f"""
                Error! User entered an invalid category. Here are the acceptable categories
                
                    Valid categories
                    -----------------
        
                        1) mean
                        2) members
                        3) spread
                        4) control
                        
                        
                Defaulting to 'mean' for now.   
            
            """)
        
    def forecast_hour_error():
        
        print(f"""
                Error! User entered a forecast hour > 240. 
                
                Defaulting to 240 as the final_forecast_hour. 
              """)