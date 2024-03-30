import cups
import create_pdf_module as ci
import os

# Bestimme das aktuelle Verzeichnis der Datei
current_file_directory = os.path.dirname(os.path.abspath(__file__))
# Pfade zu den Unterordnern relativ zur aktuellen Datei
pdf_dir_path = os.path.join(current_file_directory, "..", "assets/qr_pdf")

def print_pdf(img_path, pdf_name, printer_name="DYMO_LabelWriter_550", ):
    # Pfad zum PNG-Bild
    image_path = img_path

    # Verzeichnis für die PDF-Datei
    pdf_dir = pdf_dir_path

    # Name der PDF-Datei
    output_pdf_name = pdf_name

    # Erstellen Sie das PDF mit dem Bild und erhalten Sie den Pfad zur erstellten PDF
    pdf_path = ci.create_pdf_with_image(image_path, pdf_dir, output_pdf_name, "NutriNails")

    # Verbindung zu CUPS herstellen
    conn = cups.Connection()
    
    # Verfügbare Drucker abrufen
    printers = conn.getPrinters()
    
    # Einen Drucker auswählen
    if printer_name is None or printer_name not in printers:
        # Wenn kein Druckername angegeben wurde oder der angegebene Name ungültig ist,
        # verwende den ersten verfügbaren Drucker
        printer_name = list(printers.keys())[0]
    
    # Druckoptionen festlegen (optional, hier als Beispiel)
    print_options = {
        'fit-to-page': 'True'
    }
    
    # PDF-Datei drucken
    conn.printFile(printer_name, pdf_path, "PDF Druckauftrag", options=print_options)
    print("Druckauftrag für '{pdf_path}' wurde an '{printer_name}' gesendet.")


