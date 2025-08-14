import subprocess
import os

try:
    import winshell
except Exception as e:
    pass

def clear_recycle_bin_windows():
    
    """
    This function clears the recycle bin on Windows OS
    
    Required Arguments: None
    
    Optional Arguments: None    
    """
    
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
    except Exception as e:
        pass
    
    
    
def clear_trash_bin_mac():
    
    """
    This function clears the trash bin on Mac OS

    Required Arguments: None
    
    Optional Arguments: None        
    """
    
    try:
        # AppleScript to tell Finder to empty the Trash
        # The 'on error number -128' handles cases where the Trash is already empty,
        # preventing an error message from being displayed.
        applescript_command = """
        osascript -e 'try' -e 'tell application "Finder" to empty' -e 'on error number -128' -e 'end try'
        """
        subprocess.run(applescript_command, shell=True, check=True, capture_output=True)
    except Exception as e:
        pass
    
    
def clear_trash_bin_linux():
    
    """
    This function clears the trash bin on Linux OS

    Required Arguments: None
    
    Optional Arguments: None        
    """     
    try:
        # Execute the 'trash-empty' command
        subprocess.run(["trash-empty"], check=True)
        
    except Exception as e:
        pass
    
