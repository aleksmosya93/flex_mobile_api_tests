import pytest
import uuid
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie")
    ]

    def setup_method(self):
        data = {
            'email': 'a.mosyakin@itdept.cloud',
            'password': 'rewq4321',
            'installation_unique_id': str(uuid.uuid4())
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = MyRequests.post('/api/v4/mobile/login/', json=data, headers=headers)

        self.auth_token = self.get_auth_token(response, 'auth._token.local')
        self.refresh_token = self.get_refresh_token(response, 'auth._refresh_token.local')
        self.user_id = self.get_json_value(response, 'user', 'pk')

    @allure.description("This test successfully authorize user by email")
    def test_user_auth(self):
        cookie = {
            "Cookie": 'auth._refresh_token.local=' + self.refresh_token + ';' + 'auth._token.local=' + self.auth_token
        }
        print(cookie)
        response_user = MyRequests.get('/api/v4/mobile/user', cookies=cookie)

        Assertions.assert_json_value_by_name(response_user, 'pk', self.user_id, 'User_id from auth method is not equal to user_id from check method')

    @allure.description("THis test checks authorization status w/o sending auth cookies ")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negativ_auth_check(self, condition):
        if condition == "no_cookie":
            response_user = MyRequests.get("/api/v4/mobile/user/")

            Assertions.assert_json_value_by_name(response_user, 'detail', 'Учетные данные не были предоставлены.', "Actual detail in the response is not correct")

            assert response_user.status_code == 401

