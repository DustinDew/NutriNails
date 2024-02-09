#Import libraries
import sys
import os

# Import modules

# Directory of current file
current_file_directory = os.path.dirname(os.path.abspath(__file__))

# Path to /modules
modules_dir_path = os.path.join(current_file_directory, "..", "modules")

sys.path.append(modules_dir_path)
from gui_modules import create_gui

# Main function to start the program
def main():
    # Call the function to create the GUI
    create_gui()

# Ensure that the main function is only called when the script is run directly
if __name__ == "__main__":
    main()
