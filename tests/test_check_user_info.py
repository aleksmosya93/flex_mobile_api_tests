import pytest
import requests
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserInfo:
    cookies = [
        ('auth._refresh_token.local=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxNTg4OTYsInVzZXJuYW1lIjoiYWxleG0iLCJleHAiOjE3MTMxODU0NjQsImVtYWlsIjoiYS5tb3N5YWtpbkBpdGRlcHQuY2xvdWQifQ.q3kzFTRHefLTogTKe8rQmvMZ6qOwLB8ggiJ-td9ajZBZFvbOyJeZfFOHNmj-NQumM49Szap9EsHjQN7B1TR2rA; auth._token.local=JWT%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNTg4OTYsInVzZXJuYW1lIjoiYWxleG0iLCJleHAiOjE2ODQ4MDMwNjQsImVtYWlsIjoiYS5tb3N5YWtpbkBpdGRlcHQuY2xvdWQifQ.V4Oub1NHIQbXpI4Q_5-JK66E__EwHr6XPukCTLvVhLY'),
        ('')
    ]

    @pytest.mark.parametrize('cookie', cookies)
    def test_check_user_info(self, cookie):
        cookie = {
            "Cookie": cookie
        }
        response = MyRequests.get('/api/v4/mobile/user/', cookies=cookie)

        if response.status_code == 200:
            expected_fields = ['email', 'pk', 'username']

            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_keys(response, expected_fields)
            Assertions.assert_json_value_by_name(
                response,
                'email',
                'a.mosyakin@itdept.cloud',
                'Actual email in the response is not correct'
            )

        else:
            Assertions.assert_code_status(response, 401)
            Assertions.assert_json_has_key(response, 'detail')
            Assertions.assert_json_value_by_name(
                response,
                'detail',
                'Учетные данные не были предоставлены.',
                'Actual detail in the response is not correct'
            )