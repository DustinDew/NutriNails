import streamlit as st
from PIL import Image
import os
import sys
import cv2
import numpy as np

# Bestimme das aktuelle Verzeichnis der Datei
current_file_directory = os.path.dirname(os.path.abspath(__file__))
# Pfade zu den Unterordnern relativ zur aktuellen Datei
images_dir_path = os.path.join(current_file_directory, "..", "assets/images")
modules_dir_path = os.path.join(current_file_directory, "..", "modules")

# Füge den Pfad zu den Modulen zum Systempfad hinzu
sys.path.append(modules_dir_path)
# Importiere lokale Module
from finger_tip_tracking_module import ft_tracking
import save_image_module as si
import generate_qrCode_module as qr
import print_label_module as pr

def main():
    st.title("NutriNails")
    st.sidebar.title("Funktionen")

    # Initialisiere eine Session State Variable für die aktuelle Auswahl, falls noch nicht vorhanden
    if 'current_function' not in st.session_state:
        st.session_state.current_function = None

    # Sidebar-Buttons für die Funktionen
    sidebar_options = {
        "Linke Hand": "left_hand",
        "Linke Hand Daumen": "left_thumb",
        "Rechte Hand": "right_hand",
        "Rechte Hand Daumen": "right_thumb",
        "Handtracking Test": "ht_test",
        "Bildeinstellungen": "img_settings"
    }

    for option, value in sidebar_options.items():
        if st.sidebar.button(option):
            st.session_state.current_function = value

    # Funktionen basierend auf der aktuellen Auswahl ausführen
    if st.session_state.current_function == "left_hand":
        take_and_save_image("Linke Hand", "LH")
    elif st.session_state.current_function == "left_thumb":
        take_and_save_image("Linke Hand Daumen", "LHD")
    elif st.session_state.current_function == "right_hand":
        take_and_save_image("Rechte Hand", "RH")
    elif st.session_state.current_function == "right_thumb":
        take_and_save_image("Rechte Hand Daumen", "RHD")
    elif st.session_state.current_function == "img_settings":
        manage_img_settigns()
    elif st.session_state.current_function == "ht_test":
        hand_tracking()
    
    

def take_and_save_image(hand_type, label):
    
    st.header(f"{hand_type} aufnehmen")
    # Nutze st.camera_input für die Bildaufnahme
    captured_image = st.camera_input(f"Klicke, um ein Bild der {hand_type} aufzunehmen")

    if captured_image is not None:
        # Sobald ein Bild aufgenommen wurde, zeige es an
        image = Image.open(captured_image)
        st.image(image, caption=f"{hand_type} Aufgenommenes Bild", use_column_width=True)

        # Button zum Speichern des Bildes, erscheint nur nach der Bildaufnahme
        if st.button(f"{hand_type} Bild speichern"):
            # Speichere das Bild und führe weitere Aktionen aus
            si.save_image(image, label)
            qrcode = qr.generate_qr_code(label)
            pr.print_pdf(qrcode[0], qrcode[1])
            st.success(f"{hand_type} Bild und QR-Code erfolgreich in {images_dir_path} gespeichert.")
           
def manage_img_settigns():
    st.title("Kamera-Einstellungen")
    st.header("Helligkeitseinstellungen")
    brightness_value = st.slider("Helligkeit", min_value=0, max_value=255, value=128, step=1)

    st.header("Sättigung")
    saturation = st.slider("Sättigung", min_value=0, max_value=300, value=150, step=10)
    
    
    if st.button("Anwenden"):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness_value)
        cap.set(cv2.CAP_PROP_SATURATION, saturation)
        
        cap.release()
        st.success("Änderungen wurden angewendet")

def hand_tracking():
    st.title("Handtracking-Demo")

    # Kamera-Input von Streamlit
    image_file = st.camera_input("Nehmen Sie Ihre Hand auf")

    if image_file:
        # Konvertieren des Uploads in ein PIL-Bild
        image_pil = Image.open(image_file)

        # Verarbeiten des Bildes
        processed_image = ft_tracking(image_pil)

        # Anzeigen des verarbeiteten Bildes
        st.image(processed_image, caption="Verarbeitetes Bild")

if __name__ == "__main__":
    main()
