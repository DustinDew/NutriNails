# Import libraries
import hashlib
from datetime import datetime

# Function to generate a unique hash value for image identification
def generate_img_hash():
    # Get current timestamp as data
    data = str(datetime.now())
    
    # Select the hash algorithm (SHA-256 currently)
    hasher = hashlib.sha256()
    
    # Update the hash with the current data
    hasher.update(data.encode("utf-8"))
    
    # Get the hexadecimal representation of the first 32 characters of the hash
    img_hash = hasher.hexdigest()[:32]
    
    # Return the hexadecimal value of the hash
    return img_hash