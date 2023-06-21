import json.decoder
from datetime import datetime
from requests import Response

class BaseCase:
    def get_auth_token(self, response: Response, auth_token):
        assert auth_token in response.cookies, f"Cannot find cookie with name {auth_token} in the last response"
        return response.cookies[auth_token]

    def get_refresh_token(self, response: Response, refresh_token):
        assert refresh_token in response.cookies, f"Cannot find cookie with name {refresh_token} in the last response"
        return response.cookies[refresh_token]

    def get_json_value(self, response: Response, name, name_2):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecoder:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        assert name_2 in response_as_dict[name], f"Response JSON doesn't have key '{name_2}'"

        return response_as_dict[name][name_2]

    def prepare_registration_data_email(self, email=None, code=None):
        if email is None:
            base_part = 'aqamobileflex'
            domain = 'gmail.com'
            random_part = datetime.now().strftime('%m%d%Y')
            email = f'{base_part}+{random_part}@{domain}'
        return {
            'email': email,
            'password1': 'rewq4321',
            'code': code
        }