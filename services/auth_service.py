import requests

import settings

class AuthService:
    @staticmethod
    def request_code(email: str):
        url = 'http://auth.enotgpt.ru/api/auth/telegram/get_code/email'

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        data = {
            "password": settings.AUTH_TOKEN,
            "email": email,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(response.text)
            return None

    @staticmethod
    def auth(auth_code: int, code_id: int, email: str):
        url = 'http://auth.enotgpt.ru/api/auth/telegram/confirm_email'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        data = {
            "password": settings.AUTH_TOKEN,
            "code_id": code_id,
            "code": auth_code,
            "email": email
        }

        print(data)

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(response.content)
            return None