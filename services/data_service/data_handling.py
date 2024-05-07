def create_dictObj(): 
    data = {
                "id": "",
                "name": "",
                "email": "",
                "student_id": "",
                "sex": "",
                "age": 0,
                "check_probe": "",
                "check_contact": "",
                "RH_img": "",
                "RT_img": "",
                "LH_img": "",
                "LT_img": ""
            }
    
    return data


def populate_personData(personData_obj, name, email, student_id, sex, age, check_probe, check_contact):
    person_data = personData_obj
    person_data["name"] = name
    person_data["email"] = email
    person_data["student_id"] = student_id
    if len(sex) > 0:
        person_data["gender"] = sex[0]
    person_data["age"] = age
    person_data["check_probe"] = check_probe
    person_data["check_contact"] = check_contact

    return person_data
    
