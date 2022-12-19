import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from decorator_api import get_api_logger, post_api_logger, put_api_logger, delete_api_logger
import settings


@post_api_logger
def post_request(url, headers, data):
    return requests.post(url=url, headers=headers, data=data)


@get_api_logger
def get_request(url, headers, params=None):
    return requests.get(url=url, headers=headers, params=params)


@delete_api_logger
def delete_request(url, headers, path):
    url = url + path
    return requests.delete(url=url, headers=headers)


@put_api_logger
def put_request(url, headers, data, path):
    url = url + path
    return requests.put(url=url, headers=headers, data=data)


class PetFriendsDecorator:
    def __init__(self):
        self.base_url = settings.creds['base_url']

    def get_api_key(self, email, password):
        headers = {
            "email": email,
            'password': password
        }
        res = get_request(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        try:
            result = res.json()['key']
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        headers = {'auth_key': auth_key}

        res = get_request(self.base_url + 'api/pets', headers=headers, params="filter=" + filter)

        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet_with_photo(self, auth_key, name, animal_type, age, pet_photo):
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key, 'Content-Type': data.content_type}
        res = post_request(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        response_head = res.headers
        try:
            result = res.json()
        except:
            result = res.text
        return status, result, response_head

    def add_new_pet_simple_without_photo(self, auth_key, name, animal_type, age):
        data = MultipartEncoder(
            fields={
                "name": name,
                "animal_type": animal_type,
                "age": age,
            })
        headers = {'auth_key': auth_key, 'Content-Type': data.content_type}
        res = post_request(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def set_pet_photo(self, auth_key, pet_id, pet_photo):
        data = MultipartEncoder(
            fields={
                'pet_id': pet_id,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key, 'Content-Type': data.content_type}
        res = post_request(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def change_pet(self, auth_key, pet_id, name, animal_type, age):
        data = MultipartEncoder(
            fields={
                "name": name,
                "animal_type": animal_type,
                "age": age,
            })
        headers = {'auth_key': auth_key, 'Content-Type': data.content_type}
        res = put_request(self.base_url + 'api/pets/', headers=headers, data=data, path=pet_id)
        status = res.status_code
        response_head = res.headers
        try:
            result = res.json()
        except:
            result = res.text
        return status, result, response_head

    def delete_pet(self, auth_key, pet_id):
        headers = {'auth_key': auth_key}

        res = delete_request(self.base_url + "api/pets/", headers=headers, path=pet_id)
        response_head = res.headers
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result, response_head

    def add_new_pet_simple_without_photo_without_animal_type_field(self, auth_key, name, age):
        data = MultipartEncoder(
            fields={
                "name": name,
                "age": age,
            })
        headers = {'auth_key': auth_key, 'Content-Type': data.content_type}
        res = post_request(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
