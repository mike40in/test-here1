import pytest
import json
import requests
from main import PetFriends
from requests_toolbelt import MultipartEncoder
from settings import valid_email, valid_password, invalid_password, invalid_email

pf = PetFriends()
key = pf.get_api_key(valid_email, valid_password)[1]['key']
# Позитивные тесты


def test_positive_valid_api(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_positive_get_list_of_pets(auth_key=key, filter=""):
    status, result = pf.get_list_of_pets(auth_key, filter=filter)
    assert status == 200
    assert "pets" in result


def test_positive_post_info_without_picture(auth_key=key, name='lesha', animal_type='Пингвин', age='4'):
    status, result = pf.post_information_about_pet_without_picture(
        auth_key, name, animal_type, age)
    assert status == 200


def test_positive_delete_pet(auth_key=key, pet_id='60b3a9f9-0f45-4ab7-9827-ebd819000062'):
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status == 200


def test_positive_post_info_with_picture(auth_key=key, name='Леха', animal_type='осьминог', age='34', pet_photo='images/pop-cat.jpg'):
    status = pf.post_information_with_picture(
        auth_key, name, animal_type, age, pet_photo)
    assert status == 200


def test_positive_set_pet_photo(auth_key=key, pet_id='9b19d623-3fe7-4b63-a69a-8c5862e7ec77', pet_photo='images/longcat.jpg'):
    status, result = pf.set_pet_photo(auth_key, pet_id, pet_photo)
    assert status == 200


def test_positive_update_info(auth_key=key, pet_id='9b19d623-3fe7-4b63-a69a-8c5862e7ec77', name='Олег', animal_type='Крокодил', age='89'):
    status, result = pf.update_information_about_pet(
        auth_key, pet_id, name, animal_type, age)
    assert status == 200

# Негативные тесты


def test_negative_valid_api(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status != 403


def test_nagative_get_list_of_pets(auth_key=key, filter='my_pets'):
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status != 403 or status != 402


def test_negative_delete_pet(auth_key=key, pet_id="9b19d623-3fe7-4b63-a69a-8c5862e7ec77"):
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status != 403 or status != 402


def test_negative_set_pet_photo(auth_key=key, pet_id='b47669c9-7a7e-44ce-8c6f-7b0e9b41b290', pet_photo='images/longcat.jpg'):
    status, result = pf.set_pet_photo(auth_key, pet_id, pet_photo)
    assert status != 403 or status != 402