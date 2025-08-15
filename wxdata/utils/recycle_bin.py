"""
This file hosts functions that clear recycle/trash bins on different OS to preserve memory.

(C) Eric J. Drewitz 2025
"""

import subprocess
import ctypes

    
def clear_recycle_bin_windows(confirm=False, show_progress=False, sound=False):
    """
    Empties the Recycle Bin.

    Args:
        confirm (bool): If True, displays a confirmation dialog.
        show_progress (bool): If True, displays a progress dialog during deletion.
        sound (bool): If True, plays a sound when the operation is complete.
    """
    # Define flags for SHEmptyRecycleBin
    flags = 0
    if not confirm:
        flags |= 0x00000001  # SHERB_NOCONFIRMATION
    if not show_progress:
        flags |= 0x00000002  # SHERB_NOPROGRESSUI
    if not sound:
        flags |= 0x00000004  # SHERB_NOSOUND

    # Call the SHEmptyRecycleBin function
    result = ctypes.windll.shell32.SHEmptyRecycleBinA(None, None, flags)

    if result == 0:  # S_OK
        pass
    else:
        print(f"Failed to empty Recycle Bin. Recycle Bin Already Empty")
    
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
    
