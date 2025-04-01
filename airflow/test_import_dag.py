import sys
from pathlib import Path

# Add the directories to sys.path for testing import
sys.path.append(str(Path(__file__).parents[1]))  # Adding the parent directory (root folder)
sys.path.append(str(Path(__file__).parents[0]))  # Adding the current directory

# Test the import and display some content
try:
    # Attempt to import the required module
    from python_code.services.runallupdates import run_all_updates

    # If import is successful, display some information from the module
    print("✅ Import successful!")
    print("Here is the content of the 'run_all_updates' function:")
    
    # Displaying the function itself or the docstring to confirm it's the right function
    print(run_all_updates.__doc__)  # This prints the docstring if present
    
    # You can also display some other part of the module if needed
    print("\nList of functions inside the module:")
    print(dir(run_all_updates))  # This prints all the functions and variables in the module

except ImportError as e:
    print("❌ Import failed:", e)
