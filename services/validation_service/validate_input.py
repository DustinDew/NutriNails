import re

def val_input_data(name, email, student_id):
    name_result = val_name(name)
    email_result = val_email(email)
    student_id_result = val_studentID(student_id)
    

    return name_result & email_result & student_id_result 
    


def val_name(name):
    if name == "":
        return True
    
    valid_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for char in name:
        if char not in valid_characters:
            return False
        return True
    

def val_email(email):
    if email == "":
        return True

    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.]+\.hs-fulda.de$'
    if re.match(pattern, email):
        return True
    return False

def val_studentID(student_id):
    if student_id == "":
        return True
    
    pattern = r'^fd(ai|et|gw|lt|oe|sk|sw|w)\d{1,4}$'
    if re.match(pattern, student_id):
        return True
    return False