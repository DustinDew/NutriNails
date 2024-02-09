# Import libraries
import tkinter as tk
import subprocess
import os
import sys

# Import modules
from capture_image_module import capture_image

#Relativ path for system independency
# Directory of current file
current_file_directory = os.path.dirname(os.path.abspath(__file__))
# Path to /modules
images_dir_path = os.path.join(current_file_directory, "..", "assets/images")

# Function to capture an image
def on_button_click():
    capture_image()

# Function to open the specified folder
def on_open_folder_click(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        print("Opening folder:", folder_path)
        subprocess.run(["xdg-open", folder_path])
    else:
        print("The folder does not exist")

# Function to exit the programm
def on_exit_click(root):
    print("Exiting the programm")
    root.destroy()

# Main GUI function
def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("NutriNails")

    # Set window size
    root.geometry("400x300")

    # Define folder path
    specific_folder_path = images_dir_path

    # Capture button
    button_run_script = tk.Button(root, text="Capture", command=on_button_click)
    button_run_script.pack(pady=20)
    
    # Open folder button
    button_open_folder = tk.Button(root, text="Open Folder", command=lambda: on_open_folder_click(specific_folder_path))
    button_open_folder.pack(pady=20)
    
    #Exit button
    button_exit = tk.Button(root, text="Exit", command =lambda: on_exit_click(root))
    button_exit.pack(pady=20)
    
    # Start the GUI
    root.mainloop()