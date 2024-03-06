import streamlit as st
from PIL import Image
import os 
import sys

# Bestimme das aktuelle Verzeichnis der Datei
current_file_directory = os.path.dirname(os.path.abspath(__file__))
# Pfade zu den Unterordnern relativ zur aktuellen Datei
images_dir_path = os.path.join(current_file_directory, "..", "assets/images")
modules_dir_path = os.path.join(current_file_directory, ".." , "modules")

# Füge den Pfad zu den Modulen zum Systempfad hinzu
sys.path.append(modules_dir_path)
# Importiere lokale Module
import save_image_module as si
import generate_qrCode_module as qr
import print_label_module as pr

def main():
    st.title("NutriNails")
    # Nutze st.camera_input für die Bildaufnahme
    captured_image = st.camera_input("Klicke, um ein Bild aufzunehmen")

    if captured_image is not None:
        # Konvertiere das aufgenommene Bild zu einem PIL-Image
        image = Image.open(captured_image)
        # Zeige das aufgenommene Bild in der Streamlit-App an
        st.image(image, caption="Aufgenommenes Bild", use_column_width=True)
        # Speichere das Bild mit einem gewünschten Dateinamen
        si.save_image(image)
        # Generiere den QR-Code für das aufgenommene Bild
        qrcode = qr.generate_qr_code()
        pr.print_pdf(qrcode[0], qrcode[1])
        st.success(f"Bild und QR-Code erfolgreich in {images_dir_path} gespeichert.")

if __name__ == "__main__":
    main()
