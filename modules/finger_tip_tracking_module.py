import cv2 as cv
import mediapipe as mp
import numpy as np

def ft_tracking(image_pil):
    # MediaPipe Initialisierung
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    # Initialisieren von MediaPipe Hands
    hand = mp_hands.Hands()

    # Liste der Indizes für die Fingerspitzen (ohne den Daumen)
    finger_tips_indices = [4, 8, 12, 16, 20]

    # Konvertieren des PIL-Bildes in ein NumPy-Array, das von OpenCV verwendet werden kann
    image_np = np.array(image_pil)

    # OpenCV arbeitet standardmäßig mit BGR-Bildern, aber PIL gibt ein RGB-Bild zurück
    # Also konvertieren wir von RGB nach BGR
    image = cv.cvtColor(image_np, cv.COLOR_RGB2BGR)

    # Konvertieren des Bildes in RGB für die Verarbeitung mit MediaPipe
    RGB_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    # Bild durch MediaPipe verarbeiten
    result = hand.process(RGB_image)

    # Überprüfen, ob Hände im Bild gefunden wurden
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Zeichnen nur der Fingerspitzen basierend auf ihren Indizes
            for idx in finger_tips_indices:
                x = int(hand_landmarks.landmark[idx].x * image.shape[1])
                y = int(hand_landmarks.landmark[idx].y * image.shape[0])
                cv.circle(image, (x, y), 18, (255, 0, 255), 2)

    # Das verarbeitete Bild zurück in das RGB-Format konvertieren, um es in Streamlit anzuzeigen
    processed_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    return processed_image
