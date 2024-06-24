import requests
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
import label_printer_service.generate_qrCode as qr
import label_printer_service.print_label as pr 

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

    if "hash_code" not in st.session_state:
        hash_code = generate_img_hash()
        st.session_state.hash_code = hash_code
    
    
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
        
        if st.button("Call API"):
            data = requests.get("https://0.0.0.0:8000/takeImg", verify=False).json()
            st.write(data)
            
        with st.form("user_inputData", clear_on_submit= True):

            
            check_print2 = st.checkbox("QR-Code drucken", value= True)
            submitted = st.form_submit_button("Teilnehmer abschließen")
            
            if submitted:
                if True: #st.session_state['checkbox_values']['LH'] == True & st.session_state['checkbox_values']['LT'] == True & st.session_state['checkbox_values']['RH'] == True & st.session_state['checkbox_values']['RT'] == True:
                    
                    if check_print2:
                        
                        qrcode = qr.generate_qr_code(st.session_state.current_function, st.session_state.hash_code)
                        
                        pr.print_pdf(qrcode[0], qrcode[1], st.session_state.hash_code)

                    st.success("Abschluss erfolgreich!")
                    
                    
                    ## ------ Schnittstelle Backend ------ ##
                    
                    ## ------ ##

                    time.sleep(2)
                    st.session_state.person_data = create_dictObj()
                    st.session_state.current_function = "left_hand"
                    st.session_state['checkbox_values'] = {"LH" : False, "LT" : False, "RH" : False, "RT" : False}

                    new_hash = generate_img_hash()
                    st.session_state.hash_code = new_hash
                    st.session_state['person_data'] = populate_personData(st.session_state["person_data"], new_hash) 
                    print(st.session_state["person_data"])

                    st.rerun()
                
                
        

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
                image_path = si.save_image(st.session_state.cap_image, label, st.session_state.hash_code)
                
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

def capture_Image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Fehler beim Öffnen der Webcam")
        return None
      
    
    ret, frame = cap.read()
    if not ret:
        st.error("Fehler beim Aufnehmen des Bildes")
        return None
        
    cap.release()
    return frame

def manage_img_settigns():
    if st.button("Bild aufnehmen"):
        frame = capture_Image()
        if frame is not None:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(rgb_frame, channels="RGB")

        

        

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
