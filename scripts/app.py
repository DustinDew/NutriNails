import os
import sys 
import time 
import tkinter as tk
from tkinter import Label, Text
from tkinter import messagebox
import cv2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Event, Thread
from queue import Queue, Empty
from PIL import Image, ImageTk

# Set paths
current_file_directory = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_file_directory, "..", "assets/graphics/logo.png")
dir = os.path.join(current_file_directory, "..", "ip_server/uploads")
modules_dir_path = os.path.join(current_file_directory, "..", "services")
sys.path.append(modules_dir_path)

from image_service.image_saving_service.generate_hash import generate_img_hash
import label_printer_service.generate_qrCode as qr
import label_printer_service.print_label as pr 

# Watchdog event handler
class Watcher(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_created(self, event):
        if not event.is_directory:
            self.app.queue.put(event.src_path)
            print(f"New file created: {event.src_path}")

# Start watching function
def start_watching(directory, queue, stop_event, app):
    event_handler = Watcher(app)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    print(f"Started monitoring the directory: {directory}")

    def watch():
        try:
            while not stop_event.is_set():
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()

    thread = Thread(target=watch)
    thread.start()
    return observer, thread

# GUI application class
class FileWatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NutriNAIL")
        self.root.geometry("1580x900")
        self.set_icon(logo_path)
        self.queue = Queue()
        self.stop_event = Event()
        self.observer = None
        self.observer_thread = None
        self.new_files = ["", "", "", "", ""]
        self.hashcode = generate_img_hash()
        self.is_watching = False
        self.cap = None
        self.setup_gui()
        self.check_queue()
        self.init_webcam()

    def set_icon(self, icon_path):
        if os.path.exists(icon_path):
            icon = ImageTk.PhotoImage(file=icon_path)
            self.root.iconphoto(False, icon)
        else:
            print(f"Icon file not found: {icon_path}")


    def setup_gui(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Frame for Buttons
        button_frame = tk.Frame(main_frame, bg="#63807a", padx=20, pady=20)
        button_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Logo
        logo_img = Image.open(logo_path)  # Update with the correct path to your logo
        logo_img = logo_img.resize((180, 180))  # Resize the logo if necessary
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = Label(button_frame, image=logo_photo)
        logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
        logo_label.pack(anchor="n", pady=10)

        # Start Watch Button
        self.start_btn = tk.Button(button_frame, text="Start", command=self.start_watching, width=20, height=2)
        self.start_btn.pack(pady=20)

        # Print Button
        self.print_btn = tk.Button(button_frame, text="Label Drucken", command=self.print_label, width=20, height=2)
        self.print_btn.pack(pady=20)

        # Reset Button
        self.reset_btn = tk.Button(button_frame, text="Teilnehmer Beenden", command=self.reset, width=20, height=2)
        self.reset_btn.pack(pady=20)

        # Frame for the rest of the content
        content_frame = tk.Frame(main_frame)
        content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Frame for Listbox and Webcam
        top_frame = tk.Frame(content_frame)
        top_frame.pack(fill="x")

        # Listbox to display new files
        self.file_listbox = tk.Listbox(top_frame, width=50)
        self.file_listbox.pack(side="left", padx=50, pady=5)

        # Webcam feed label
        self.webcam_label = tk.Label(top_frame)
        self.webcam_label.pack(side="right", padx=50, pady=5)
        


        # Frame to display images
        self.img_label = tk.Label(content_frame, text="Bildaufnahmen:")
        self.img_label.pack(pady=10)
        self.image_frame = tk.Frame(content_frame, bg="lightgrey", height= 400)
        self.image_frame.pack(pady=10, fill="both", expand=True)

       # Buttons frame
        self.buttons_frame = tk.Frame(content_frame)
        self.buttons_frame.pack(pady=10, fill="x", expand=True)

        # Additional Buttons
        self.button1 = tk.Button(self.buttons_frame, text="Button 1", width=15, height=2, command=lambda: self.replace_file(0))
        self.button2 = tk.Button(self.buttons_frame, text="Button 2", width=15, height=2, command=lambda: self.replace_file(1))
        self.button3 = tk.Button(self.buttons_frame, text="Button 3", width=15, height=2, command=lambda: self.replace_file(2))
        self.button4 = tk.Button(self.buttons_frame, text="Button 4", width=15, height=2, command=lambda: self.replace_file(3))

        self.button1.pack(side="left", expand=True, padx=5, pady=5)
        self.button2.pack(side="left", expand=True, padx=5, pady=5)
        self.button3.pack(side="left", expand=True, padx=5, pady=5)
        self.button4.pack(side="left", expand=True, padx=5, pady=5)


        # Label for monitoring status
        self.status_label = tk.Label(content_frame, text="Angehalten", fg="red")
        self.status_label.pack()

    def start_watching(self):
        if self.observer:
            self.stop_event.set()
            self.observer_thread.join()
            self.observer, self.observer_thread = None, None
            self.stop_event = Event()
            self.queue = Queue()
            self.is_watching = False
            self.status_label.config(text="Angehalten", fg="red")

        self.observer, self.observer_thread = start_watching(dir, self.queue, self.stop_event, self)
        self.is_watching = True
        self.status_label.config(text="Warten auf neue Dateien...", fg="green")

    def reset(self):
        if len(self.new_files) >= 4:

            try:
                self.print_label()
                self.rename_files()
                self.new_files = []
                self.hashcode = generate_img_hash()
                self.file_listbox.delete(0, tk.END)
                for widget in self.image_frame.winfo_children():
                    widget.destroy()
                self.status_label.config(text="Warten auf neue Dateien...", fg="green")
                messagebox.showinfo("Erfolg", "Die Bildaufnahmen wurden erfolgreich umbenannt und gespeichert!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occoured: {e}")
        else:
            messagebox.showinfo("Achtung", "Bildaufnahmen unvollständig!")
    
    def check_new_files(self):
        try:
            while True:
                file_path = self.queue.get_nowait()
                self.new_files.append(file_path)
                self.file_listbox.insert(tk.END, file_path)
                self.display_image(file_path)
        except Empty:
            pass

    def print_label(self):
        qrcode = qr.generate_qr_code(self.hashcode)
        pr.print_pdf(qrcode[0], qrcode[1], self.hashcode)

    def display_image(self, file_path):
        img = Image.open(file_path)
        img = img.resize((300, 360))
        photo_img = ImageTk.PhotoImage(img)
        panel = Label(self.image_frame, image=photo_img)
        panel.image = photo_img  # Keep a reference to avoid garbage collection
        panel.pack(side="left", padx=10, pady=10)

    def check_queue(self):
        self.check_new_files()
        self.root.after(1000, self.check_queue)  # Check the queue every second

    def rename_files(self):
        hand_labels = ["err", "rd", "rh", "ld", "lh"]
        for file_path in self.new_files[:]:
            try:
                filename = os.path.basename(file_path)
                new_filename = f"img_{self.hashcode}_{hand_labels[len(self.new_files)]}"
                new_filepath = os.path.join(dir, new_filename + ".png")
                os.rename(file_path, new_filepath)
                print(f"File successfully renamed from {file_path} to {new_filepath}.")
            except FileNotFoundError:
                print(f"The file {file_path} was not found.")
            except PermissionError:
                print(f"No permission to rename the file {file_path}.")
            except Exception as e:
                print(f"An error occurred: {e}")

            self.new_files.remove(file_path)

    def init_webcam(self):
        self.cap = cv2.VideoCapture(0)  # Initialize the webcam
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            self.cap = None
        else:
            self.update_webcam_feed()

    def update_webcam_feed(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (350, 240))  # Resize the frame to fit the label
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.webcam_label.imgtk = imgtk
                self.webcam_label.config(image=imgtk)
        self.root.after(10, self.update_webcam_feed)  # Update every 10ms

if __name__ == "__main__":
    root = tk.Tk()
    app = FileWatcherApp(root)
    root.mainloop()
