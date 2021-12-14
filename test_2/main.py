import pytest
import json
import requests
from settings import valid_email, valid_password, invalid_password, invalid_email
from requests_toolbelt import MultipartEncoder


class PetFriends:  # Задание 1
    def __init__(self):

        self.base_url = 'https://petfriends1.herokuapp.com/'

    def get_api_key(self, email: str, password: str) -> json:

        headers = {
            'email': email,
            'password': password
        }

        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ''

        try:
            result = res.json()

        except json.decoder.JSONDecodeError:

            result = res.text

        return status, result

    def get_list_of_pets(self, auth_key, filter: str = "") -> json:
        headers = {'auth_key': auth_key}
        filter = {'filter': filter}

        res = requests.get(self.base_url + "api/pets",
                           headers=headers, params=filter)
        status = res.status_code
        result = ""

        try:
            result = res.json()

        except json.decoder.JSONDecodeError:

            result = res.text

        return status, result

    def post_information_about_pet_without_picture(self, auth_key: json, name: str, animal_type: str, age: str) -> json:

        data = MultipartEncoder(
            fields={"name": name, "animal_type": animal_type, "age": age}
        )
        # data = {

        #     'name': name,
        #     'animal_type': animal_type,
        #     'age': age
        # }

        headers = {'auth_key': auth_key, "Content-Type": data.content_type}
        res = requests.post(
            self.base_url + '/api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:

        headers = {'auth_key': auth_key}
        res = requests.delete(
            self.base_url + f'/api/pets/{pet_id}', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_information_with_picture(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = {"auth_key": auth_key, 'Content-Type': data.content_type}
        res = requests.post(self.base_url + '/api/pets',
                            headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status

    def set_pet_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = {'auth_key': auth_key, 'Content-Type': data.content_type}
        res = requests.post(
            self.base_url + f'/api/pets/set_photo/{pet_id}', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_information_about_pet(self, auth_key: json, pet_id: str, name: str, animal_type, age: str) -> json:
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            }
        )
        headers = {'auth_key': auth_key, 'Content-Type': data.content_type}
        res = requests.put(
            self.base_url + f"/api/pets/{pet_id}", headers=headers, data=data)
        status = res.status_code
        result = ''

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


pf = PetFriends()

key = pf.get_api_key(valid_email, valid_password)[1]['key']
print(key)

print(pf.post_information_about_pet_without_picture(
    key, 'John', "German Shepherd", '3'))
print(pf.delete_pet(key, 'c37452b2-d7bc-42d0-aafe-6197f93b1241'))
print(pf.delete_pet(key, 'bfbad65a-45f4-461a-9818-5b453014b16d'))
print(pf.post_information_with_picture(key, 'Pop',
                                       'Cat', '102', 'images\pop-cat.jpg'))
print(pf.get_list_of_pets(key, 'my_pets'))
print(pf.update_information_about_pet(
    key, 'f7addcb1-8689-4d0f-93a6-4f66b2318671', 'popping', 'cat', '49'))
print(pf.set_pet_photo(key, 'f7addcb1-8689-4d0f-93a6-4f66b2318671', 'images/pop-cat.jpg'))