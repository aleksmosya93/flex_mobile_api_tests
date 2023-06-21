from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
from lib.gmail.gmail_quickstart import GmailClient
from lib.my_requests import MyRequests

class TestUserRegistration(BaseCase):
    def setup_method(self):
        base_part = 'aqamobileflex'
        domain = 'gmail.com'
        random_part = datetime.now().strftime('%m%d%Y')
        self.email = f'{base_part}+{random_part}@{domain}'

        g = GmailClient()
        self.code = g.get_activation_code()

    def test_send_code_email(self):
        data = {
            "email": self.email,
            "reset": False
        }

        response = MyRequests.post('/api/v4/mobile/auth/send-code/', json=data)
        print(data)

        Assertions.assert_code_status(response, 201)

    def test_create_user_successfully(self):
        data = self.prepare_registration_data_email(code=self.code)
        response = MyRequests.post('/api/v4/mobile/auth/registration/', json=data)

        Assertions.assert_code_status(response, 201)

    def test_create_user_with_existing_email(self):
        data = self.prepare_registration_data_email(self.email)
        response = MyRequests.post('/api/v4/mobile/auth/registration/', json=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            'email',
            ["Пользователь с таким email уже существует"],
            f'Unexpected response text {response.text}'
        )
