# Beispiel für ein Python-Skript, das OpenCV verwendet, um auf die Kamera zuzugreifen und Einstellungen anzupassen
import cv2
def changeSettings():
    # Zugriff auf die Kamera
    cap = cv2.VideoCapture(0)

    # Beispiel: Ändern der Belichtung
    cap.set(cv2.CAP_PROP_EXPOSURE, -2)

    # Beispiel: Ändern der ISO-Einstellung
    cap.set(cv2.CAP_PROP_ISO_SPEED, 400)

    # Beispiel: Ändern des Weißabgleichs
    cap.set(cv2.CAP_PROP_AUTO_WB, 0)
    cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 1000)



    # Schließen der Kamera
    cap.release()
