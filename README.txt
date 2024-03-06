# NutriNails Project (OUTDATED)

This project captures images using an external camera and provides a simple GUI to interact with the application.

## Requirements

Ensure you have the following Python libraries installed:

- 'opencv-python': For image capturing and processing.
- 'pygame': For playing sounds.
- 'qrcode[pill]': For generating QR codes.
- 'Pillow': Dependency for the 'qrcode' library.
- 'tkinter': GUI library (usually included with Python).

## Installation

You can install the required libraries using the `pip` command + the according library name (make sure to check documentation for the right name)


## Usage

- 1. Run the `main.py` script to start the application.
- 2. Press the `Capture` button to capture an image using an external camera
- 2.1 While in the `preview`-window press: `SPACE` to capture the image
					   `ESC` to abort the operation
- 2.2 While in the `image`-window press: `s` to save the image
					 `n` to capture a new image without saving the prior one
					 `ESC` to abort the process without saving the image
- 3. Press the `Open Folder` button to open the folder containing the captured images and generated QR codes
- 4. Press the `Exit` button to close the program