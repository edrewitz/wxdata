# Running External Python Scripts In Your Workflow With WxData

***def run_external_scripts(paths,
                         show_values=False):***

    This function automates the running of external Python scripts in the order the user lists them.
    
    Required Arguments:
    
    1) paths (String List) - A string list of the file paths to the external Python scripts
    
    *** The list must be in the order the user wants the scripts to execute.***
    
            Example
            -------
            
            run_external_scripts(f"{path_to_script1},
                                 f"{path_to_script2}")
                                 
            In this example, we have 2 scripts denoted as script 1 and script 2.
            
            Script1 will run BEFORE script2 as per the order of the path list we passed into run_external_scripts()
            
    Optional Arguments:
    
    1) show_values (Boolean) - Default=False. If the user wants to display the values returned set show_values=True. 
            
    Returns
    -------
    
    Runs external Python scripts.  
