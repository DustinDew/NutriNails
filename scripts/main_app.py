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
from generate_hash_module import generate_img_hash

placeholder = st.empty()

def main():
    st.sidebar.title("Hand Aufnahmen")
    st.title("NutriNails")
    st.header("Teilnehmer Daten")

    if 'person_data' not in st.session_state:
            st.session_state.person_data = {
                "id": "",
                "name": "",
                "email": "",
                "student_id": "",
                "sex": "",
                "age": 0,
                "check_probe": "",
                "check_contact": "",
                "RH_img": "",
                "RT_img": "",
                "LH_img": "",
                "LT_img": ""
            }
   
    with st.form("my_form", clear_on_submit= True):
        name = st.text_input(label="Name")
        student_id = st.text_input(label="Fd-Nummer")
        email = st.text_input(label="Email")
        sex_val = st.multiselect(label="Geschlecht:", options=["männlich", "weiblich", "divers"], max_selections=1, placeholder="Geschlecht wählen", )
        age = st.slider(label="Alter", min_value=0, max_value=100 ,step=1)
        check_probe_val = st.checkbox("Will eine Probe geben")
        check_contact_val = st.checkbox("Möchte kontaktiert werden")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Teilnehmer abschließen")
        if submitted:
            st.session_state.person_data["name"] = name
            st.session_state.person_data["email"] = email
            st.session_state.person_data["student_id"] = student_id
            if len(sex_val) > 0:
                st.session_state.person_data["gender"] = sex_val[0]
            st.session_state.person_data["age"] = age
            st.session_state.person_data["check_probe"] = check_probe_val
            st.session_state.person_data["check_contact"] = check_contact_val
            st.write(st.session_state["person_data"])
            st.session_state.person_data = {
                "id": "",
                "name": "",
                "student_id": "",
                "gender": "",
                "age": 0,
                "check_probe": "",
                "check_contact": "",
                "RH_img": "",
                "RT_img": "",
                "LH_img": "",
                "LT_img": ""
            }
            st.session_state.current_function = "left_hand"
        

    # Initialisiere eine Session State Variable für die aktuelle Auswahl, falls noch nicht vorhanden
    if 'current_function' not in st.session_state:
        st.session_state.current_function = None

    # Sidebar-Buttons für die Funktionen
    sidebar_options = {
        "Linke Hand": "left_hand",
        "Linke Hand Daumen": "left_thumb",
        "Rechte Hand": "right_hand",
        "Rechte Hand Daumen": "right_thumb",
    }

    for option, value in sidebar_options.items():
        if st.sidebar.button(option):
            st.session_state.current_function = value
    st.sidebar.title("Weiter Funktionen")
    if st.sidebar.button("Handtracking Test"):
            st.session_state.current_function = "ht_test"
    if st.sidebar.button("Bildeinstellungen"):
            st.session_state.current_function = "img_settings"

    # Funktionen basierend auf der aktuellen Auswahl ausführen
    
    if st.session_state.current_function == "left_hand":
        take_and_save_image("Linke Hand", "LH")
    elif st.session_state.current_function == "left_thumb":
        take_and_save_image("Linke Hand Daumen", "LT")
    elif st.session_state.current_function == "right_hand":
        take_and_save_image("Rechte Hand", "RH")
    elif st.session_state.current_function == "right_thumb":
        take_and_save_image("Rechte Hand Daumen", "RT")
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
        if st.button(f"Bild speichern"):
            hash_val = generate_img_hash()          
            # Speichere das Bild und führe weitere Aktionen aus
            si.save_image(image, label, hash_val)
            qrcode = qr.generate_qr_code(label, hash_val)
            pr.print_pdf(qrcode[0], qrcode[1])
            st.success(f"{hand_type} Bild und QR-Code erfolgreich in {images_dir_path} gespeichert.")
            copy_person_data = st.session_state["person_data"]
            copy_person_data[label + "_img"] = images_dir_path
            copy_person_data["id"] = hash_val
            st.session_state["person_data"] = copy_person_data

           
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
