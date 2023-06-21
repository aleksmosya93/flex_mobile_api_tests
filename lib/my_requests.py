import requests
from lib.logger import Logger
import allure
from environment import ENV_OBJECT

class MyRequests():

    @staticmethod
    def get (url: str, json: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step((f"GET request to URL '{url}'")):
            return MyRequests._send(url, json, headers, cookies, 'GET')

    @staticmethod
    def post (url: str, json: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step((f"POST request to URL '{url}'")):
            return MyRequests._send(url, json, headers, cookies, 'POST')

    @staticmethod
    def put (url: str, json: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step((f"PUT request to URL '{url}'")):
            return MyRequests._send(url, json, headers, cookies, 'PUT')

    @staticmethod
    def delete (url: str, json: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step((f"DELETE request to URL '{url}'")):
            return MyRequests._send(url, json, headers, cookies, 'DELETE')

    @staticmethod
    def _send(url: str, data: dict, headers: list, cookies: dict, method: str):
        url = f"{ENV_OBJECT.get_base_url()}{url}"

        if cookies is None:
            cookies = {}

        Logger.add_request(url, data, headers, cookies, method)

        if method == 'GET':
            response = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, cookies=cookies)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, cookies=cookies)
        elif method == 'DELETE':
            response = requests.delete(url, json=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        Logger.add_response(response)

        return response
