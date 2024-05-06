import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import inch

def create_pdf_with_image(image_path, pdf_dir, pdf_name, text, image_scale_size=(0.7, 0.7), pdf_page_size=(2.25, 1.25), text_offset=(10, 0)):
    # Bild skalieren
    img = Image.open(image_path)
    scaled_width = int(image_scale_size[0] * 72)  # 72 DPI, also 72 Pixel pro Zoll
    scaled_height = int(image_scale_size[1] * 72)
    img = img.resize((scaled_width, scaled_height))
    
    # PDF erstellen
    pdf_path = os.path.join(pdf_dir, pdf_name)
    c = canvas.Canvas(pdf_path, pagesize=(pdf_page_size[0] * inch, pdf_page_size[1] * inch))
    
    # Bild in das PDF einfügen
    x_position = (pdf_page_size[0] * inch - scaled_width) / 4
    y_position = (pdf_page_size[1] * inch - scaled_height) / 2
    c.drawInlineImage(img, x_position, y_position, width=scaled_width, height=scaled_height)
    
    # Text neben das Bild setzen
    # Text-Offset von der rechten Seite des Bildes
    text_x_position = x_position + scaled_width + text_offset[0]
    text_y_position = y_position + (scaled_height / 2) + text_offset[1]
    c.drawString(text_x_position, text_y_position, text)
    
    # PDF speichern
    c.save()

    # Rückgabe des Pfads zur erstellten PDF
    return pdf_path
