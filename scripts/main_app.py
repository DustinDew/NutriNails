import streamlit as st
from PIL import Image
import os
import sys
import cv2
import time

## ------ Relative Dateipfade ------ ##

current_file_directory = os.path.dirname(os.path.abspath(__file__))
images_dir_path = os.path.join(current_file_directory, "..", "assets/images")
modules_dir_path = os.path.join(current_file_directory, "..", "services")
sys.path.append(modules_dir_path)

## ------ Importiere lokale Module ------ ##

from data_service.data_handling import create_dictObj, populate_personData
from image_service.finger_tip_tracking import ft_tracking
import image_service.image_saving_service.save_image as si
from image_service.image_saving_service.generate_hash import generate_img_hash
from validation_service.validate_input import val_input_data

## ------ ##

def main():
    st.sidebar.title("Hand Aufnahmen")

    ## ------ Initialisierung der Session-States ------ ##

    if 'current_function' not in st.session_state:
        st.session_state.current_function = "left_hand"

    if 'cap_image' not in st.session_state:
         st.session_state.cap_image = None

    if 'person_data' not in st.session_state:
            st.session_state.person_data = create_dictObj()

    if 'checkbox_values' not in st.session_state:
        st.session_state['checkbox_values'] = {"LH" : False, "LT" : False, "RH" : False, "RT" : False}
      
     
    ## ------ Initalisierung Spalten für Seitenlayout ------ ##

    col5, col6 = st.columns([3, 4])
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.checkbox("Linke Hand", value= st.session_state["checkbox_values"]["LH"], disabled=True)
    with col2:
        st.checkbox("Linker Daumen", value= st.session_state["checkbox_values"]["LT"], disabled=True)
    with col3:
        st.checkbox("Rechte Hand", value= st.session_state["checkbox_values"]["RH"], disabled=True)
    with col4:
        st.checkbox("Rechter Daumen", value= st.session_state["checkbox_values"]["RT"], disabled=True)  
    

    ## ------ Column mit User-InputData Form ------ ##
    
    with col5:
        st.title("NutriNails")
       
            
        with st.form("user_inputData", clear_on_submit= True):

            st.write("Teilnehmer Daten:")
            name = st.text_input(label="Name")
            student_id = st.text_input(label="Fd-Nummer")
            email = st.text_input(label="Email")
            sex_val = st.multiselect(label="Geschlecht:", options=["männlich", "weiblich", "divers"], max_selections=1, placeholder="Geschlecht wählen")
            age = st.slider(label="Alter", min_value=0, max_value=100 ,step=1)
            check_probe_val = st.checkbox("Will eine Probe geben")
            check_contact_val = st.checkbox("Möchte kontaktiert werden")

            submitted = st.form_submit_button("Teilnehmer abschließen")
            
            if submitted & val_input_data(name, email, student_id):
                if st.session_state['checkbox_values']['LH'] == True & st.session_state['checkbox_values']['LT'] == True & st.session_state['checkbox_values']['RH'] == True & st.session_state['checkbox_values']['RT'] == True:
                    st.session_state['person_data'] = populate_personData(st.session_state["person_data"], name, student_id, email, sex_val, age, check_probe_val, check_contact_val)
                            
                    #hash_val = generate_img_hash()
                    #qrcode = qr.generate_qr_code(st.session_state.current_function, hash_val)
                    #pr.print_pdf(qrcode[0], qrcode[1], "NutriNails")
                    print(st.session_state["person_data"])        
                    st.success("Abschluss erfolgreich!")
                            
                    ## ------ Schnittstelle Backend ------ ##
                    
                    ## ------ ##

                    time.sleep(2)
                    st.session_state.person_data = create_dictObj()
                    st.session_state.current_function = "left_hand"
                    st.session_state['checkbox_values'] = {"LH" : False, "LT" : False, "RH" : False, "RT" : False}
                    
                    st.rerun()
                st.error("Bildaufnahmen unvollständig!")
            if val_input_data(name, email, student_id) == False:
                 st.error("Bitte Angaben überprüfen!")     

    

    ## ------ Sidebar-Buttons und function-handling ------ ##

    sidebar_options = {
        "Linke Hand": "left_hand",
        "Linker Daumen": "left_thumb",
        "Rechte Hand": "right_hand",
        "Rechter Daumen": "right_thumb",
    }

    for option, value in sidebar_options.items():
        if st.sidebar.button(option):
            st.session_state.current_function = value
    st.sidebar.title("Weiter Funktionen")
    if st.sidebar.button("Handtracking Test"):
            st.session_state.current_function = "ht_test"
    if st.sidebar.button("Bildeinstellungen"):
            st.session_state.current_function = "img_settings"

    with col6:
        
        if st.session_state.current_function == "left_hand":
            take_and_save_image("Linke Hand", "LH")
        elif st.session_state.current_function == "left_thumb":
            take_and_save_image("Linker Daumen", "LT")
        elif st.session_state.current_function == "right_hand":
            take_and_save_image("Rechte Hand", "RH")
        elif st.session_state.current_function == "right_thumb":
            take_and_save_image("Rechter Daumen", "RT")
        elif st.session_state.current_function == "img_settings":
            manage_img_settigns()
        elif st.session_state.current_function == "ht_test":
            hand_tracking()

## ------ Funktion zum Aufnehmen und Speichern eines Bildes ------ ##

def take_and_save_image(hand_type, label):
    st.title(f"{hand_type}")
    with st.form("image_capture", clear_on_submit= True): 
        
        captured_image = st.camera_input("aufnahme", label_visibility="collapsed")

        if captured_image is not None:
            st.session_state.cap_image = Image.open(captured_image)
            
        if st.form_submit_button(f"Bild speichern"):
            if captured_image == None:
                st.error("Kein Bild aufgenommen")

            elif captured_image is not None:
                hash_val = generate_img_hash()          
                image_path = si.save_image(st.session_state.cap_image, label, hash_val)
                
                st.session_state["checkbox_values"][label] = True     
                st.session_state["person_data"][label + "_img"] = image_path
                
                if label == "LH":
                    st.session_state.current_function = "left_thumb"
                elif label == "LT":
                    st.session_state.current_function = "right_hand"
                elif label == "RH":
                    st.session_state.current_function = "right_thumb"
                
                st.rerun()

## ------ Funktion zum Ändern der Kameraeinstellungen ------ ##

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

## ------ Funktion zum Tracken der Fingerspitzen ------ ##

def hand_tracking():
    st.title("Handtracking-Demo")
    image_file = st.camera_input("Nehmen Sie Ihre Hand auf")

    if image_file:
        image_pil = Image.open(image_file)
        processed_image = ft_tracking(image_pil)
        st.image(processed_image, caption="Verarbeitetes Bild")

## ------ Main-Routine ------ ##

if __name__ == "__main__":
    main()
