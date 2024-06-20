def create_dictObj(): 
    data = {
                "id": "",
                "RH_img": "",
                "RT_img": "",
                "LH_img": "",
                "LT_img": ""
            }
    
    return data


def populate_personData(personData_obj, id):
    person_data = personData_obj
    person_data["id"] = id

    return person_data
    
