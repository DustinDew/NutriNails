import datetime
import os
from datetime import datetime
import cv2
from image_service.color_correction import color_correction

import image_service.image_saving_service.generate_hash as hs  # Modul zum Generieren von Hashes
import numpy as np

# Aktuelles Verzeichnis ermitteln
current_file_directory = os.path.dirname(os.path.abspath(__file__))

# Pfad zum Verzeichnis mit Bildern, relativ zum aktuellen Verzeichnis
images_dir_path = os.path.join(current_file_directory, "../../..", "assets/images")

def save_image(image, handType, hash_val):
    # Pfad, unter dem das Bild gespeichert werden soll
    image_path = images_dir_path
    # Erzeuge einen einzigartigen Hash für das Bild
    hash = hs.generate_img_hash()
    # Bildname mit aktueller Uhrzeit und Hash erstellen
    img_name = f"img_{hash_val}_{handType}.png"
    # Konvertiere PIL-Image (Python Imaging Library) zu einem OpenCV-Image
    open_cv_image = np.array(image)
    
    # Konvertiere RGB (Rot-Grün-Blau) zu BGR (Blau-Grün-Rot) für OpenCV
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    # Speichere das Bild im angegebenen Pfad
    #cc_image = color_correction(open_cv_image)
    cc_image = open_cv_image
    cv2.imwrite(os.path.join(image_path, img_name), cc_image)
    return os.path.join(image_path, img_name)

        