# Import libraries
import cv2
import os
import random
import pygame
from datetime import datetime

# Import modules
from generate_qrCode_module import generate_qr_code
from generate_hash_module import generate_img_hash

# Relativ path for system independency
# Directory of current file
current_file_directory = os.path.dirname(os.path.abspath(__file__))
# Relativ paths
images_dir_path = os.path.join(current_file_directory, "..", "assets/images")
sounds_dir_path = os.path.join(current_file_directory, "..", "assets/sounds")
print(str(sounds_dir_path))

def capture_image():
    # Camera configuration
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    cam.set(3, 1920)
    cam.set(4, 1080)

    # Directory for saving images
    image_path = images_dir_path

    try:
        # Preview window
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Preview could not be loaded")
                break
            
            cv2.imshow("Preview", frame)
            
            key = cv2.waitKey(1)
            if key == 27:
                
                cam.release()
                cv2.destroyAllWindows()
                
                print("Operation aborted during preview")
                return
            
            if key == ord(" "):
                break
            

        cv2.destroyAllWindows()

        # Initialize and play sound
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(sounds_dir_path, "camera.mp3"))
        pygame.mixer.music.play()

        # Capture image
        result, image = cam.read()

        if result:
            cv2.namedWindow("Image")
            x = generate_img_hash()
            img_name = f"img_{datetime.now().time().strftime('%H:%M:%S')}_{x}.png"
            
            # Display captured image
            cv2.imshow("Image", image)
            
            while True:
                key = cv2.waitKey(0)

                if key == ord("s"):
                    # Save image
                    cv2.imwrite(os.path.join(image_path, img_name), image)
                    print(f"Image saved. Time: {datetime.now().time().strftime('%H:%M:%S')}")
                    
                    # Generate QR code for the saved image
                    generate_qr_code(os.path.join(image_path, img_name),
                                     f"qr_{datetime.now().time().strftime('%H:%M:%S')}_{x}.png")
                    cv2.destroyAllWindows()
                    break

                elif key == ord("n"):
                    print(f"Image not saved. Time: {datetime.now().time().strftime('%H:%M:%S')}")
                    cv2.destroyAllWindows()
                    cam.release()
                    capture_image()
                    break

                elif key == 27:  # 'Esc' key
                    print(f"Operation aborted. Time: {datetime.now().time().strftime('%H:%M:%S')}")
                    cv2.destroyAllWindows()
                    break

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Release camera resources
        cam.release()

if __name__ == "__main__":
    # Call the main function to capture image
    capture_image()
