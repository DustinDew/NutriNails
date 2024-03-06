# Bibliotheken importieren
import qrcode
import os
import generate_hash_module as hs  # Modul zum Generieren von Hashes
from datetime import datetime

# Aktuelles Verzeichnis ermitteln
current_file_directory = os.path.dirname(os.path.abspath(__file__))

# Pfad für den Ordner, in dem die Bilder gespeichert werden, relativ zum aktuellen Verzeichnis
images_dir_path = os.path.join(current_file_directory, "..", "assets/qr_images")

def generate_qr_code():
    # QR-Code Generator mit spezifizierten Parametern initialisieren
    qr = qrcode.QRCode(
        version=1,  # Version des QR-Codes (1-40) bestimmt die Größe des QR-Codes
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Fehlerkorrekturlevel (L, M, Q, H)
        box_size=10,  # Größe jeder Box/Quadrat im QR-Code
        border=4,  # Breite des Randes um den QR-Code
    )

    # Aktuelle Zeit für den Dateinamen formatieren, Sekunden und Mikrosekunden werden ignoriert
    time = datetime.now().replace(second=0, microsecond=0).strftime("%H:%M") + "_"
    filename = hs.generate_img_hash()  # Generiert einen einzigartigen Hash-Wert für den Dateinamen
    
    # Daten zum QR-Code hinzufügen
    qr.add_data("https://github.com/DustinDew/NutriNails")
    qr.make(fit=True)  # QR-Code Größe anpassen, um die Daten zu passen
    
    # QR-Code als Bild generieren, Farben definieren
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Das Bild in einer Datei speichern
    output_path = os.path.join(images_dir_path, "qr_" + time + str(filename))
    img.save(output_path)
    return_arr = [output_path, "qr_" + time + str(filename)]
    return return_arr
