#Import libraries
import sys

# Import modules
sys.path.append("/home/raspi/developement/project_NutriNails/modules")
from gui_modules import create_gui

# Main function to start the program
def main():
    # Call the function to create the GUI
    create_gui()

# Ensure that the main function is only called when the script is run directly
if __name__ == "__main__":
    main()
