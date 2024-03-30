import os
from datetime import datetime
import cv2
from color_correction_module import color_correction
import generate_qrCode_module as qr  # Modul zum Generieren von QR-Codes
import generate_hash_module as hs  # Modul zum Generieren von Hashes
import numpy as np
from PIL import Image

# Aktuelles Verzeichnis ermitteln
current_file_directory = os.path.dirname(os.path.abspath(__file__))

# Pfad zum Verzeichnis mit Bildern, relativ zum aktuellen Verzeichnis
images_dir_path = os.path.join(current_file_directory, "..", "assets/images")

def save_image(image, handType):
    # Pfad, unter dem das Bild gespeichert werden soll
    image_path = images_dir_path
    # Erzeuge einen einzigartigen Hash für das Bild
    hash = hs.generate_img_hash()
    # Bildname mit aktueller Uhrzeit und Hash erstellen
    img_name = f"img_{handType}_{datetime.now().time().strftime('%H:%M:%S')}_{hash}.png"
    # Konvertiere PIL-Image (Python Imaging Library) zu einem OpenCV-Image
    open_cv_image = np.array(image)
    
    # Konvertiere RGB (Rot-Grün-Blau) zu BGR (Blau-Grün-Rot) für OpenCV
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    # Speichere das Bild im angegebenen Pfad
    cc_image = color_correction(open_cv_image)
    cv2.imwrite(os.path.join(image_path, img_name), cc_image)


        