"""
This file hosts the function on automating external Python scripts

(C) Eric J. Drewitz 2025
"""

import subprocess
import sys
import os

def run_external_scripts(paths,
                         return_values=False,
                         show_values=False):
    
    """
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
    
    1) return_values (Boolean) - Default=False. If the user wishes to return values from the external script, set return_values=True.
    
    2) show_values (Boolean) - Default=False. If the user wants to display the values returned set show_values=True. 
            
    Returns
    -------
    
    Runs external Python scripts.    
    """
    
    for path in paths:
        command = [sys.executable, path]

        fname = os.path.basename(path)
        
        try:
            if return_values == False:
                subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            else:
                result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, capture_output=True)
                if show_values == True:
                    print(result)
                else:
                    pass
            print(f"{fname} ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Script failed with return code {e.returncode}. Error:")
            print(e.stderr)
        except FileNotFoundError:
            print(f"Error: Could not find the python executable or the script file.")