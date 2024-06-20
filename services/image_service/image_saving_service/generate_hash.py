# Bibliotheken importieren
import hashlib  
from datetime import datetime  

# Funktion zur Generierung eines einzigartigen Hash-Werts für die Bildidentifikation
def generate_img_hash():
    # Den aktuellen Zeitstempel als Datenbasis nutzen
    data = str(datetime.now())
    
    # Auswahl des Hash-Algorithmus (hier SHA-256)
    hasher = hashlib.sha256()
    
    # Den Hash mit den aktuellen Daten aktualisieren
    hasher.update(data.encode("utf-8"))  # Die Daten müssen in Bytes umgewandelt werden
    
    # Die hexadezimale Darstellung der ersten 16 Zeichen des Hashs erhalten
    img_hash = hasher.hexdigest()[:8]
    
    # Den hexadezimalen Wert des Hashs zurückgeben
    return img_hash
