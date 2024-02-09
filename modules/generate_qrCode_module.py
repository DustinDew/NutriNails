# Import libraries
import qrcode
import os

def generate_qr_code(data, filename):
    # Create a QR-Code generator with specified parameters
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the QR-Code
    qr.add_data(data)
    qr.make(fit=True)
    
    # Generate the QR-Code as an image
    img = qr.make_image(fill_color="black", black_color="white")
    
    # Save the image to a file
    output_path = os.path.join("/home/raspi/developement/project_NutriNails/assets/images", filename)
    img.save(output_path)
    