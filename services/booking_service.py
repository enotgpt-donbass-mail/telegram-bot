from datetime import datetime

import requests

import settings
from utils.date_formatter import format_custom_date


class BookingService:
    base_url = 'https://misha.enotgpt.ru'

    @staticmethod
    def make_request(route: str) -> dict | None:
        url = f'{BookingService.base_url}{route}'

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {settings.AUTH_TOKEN}'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()

        else:
            print(f'Error from backend: {response.text}')
            return None

    @staticmethod
    def get_post(index: str) -> dict | None:
        url = f'/offices/get_by_index?index={int(index)}'
        return BookingService.make_request(url)

    @staticmethod
    def get_posts() -> dict | None:
        url = f'/offices/get'
        return BookingService.make_request(url)

    @staticmethod
    def get_post_by_subcategory_id(subcategory_id: int) -> dict | None:
        url = f'/offices/getOfficesByCategory?operation_role_id={subcategory_id}'
        return BookingService.make_request(url)

    @staticmethod
    def get_operations() -> dict | None:
        url = f'/operation_roles/get'
        return BookingService.make_request(url)

    @staticmethod
    def get_reserve() -> dict | None:
        url = f'/reserved/getAll?limit=100000&offset=0'
        return BookingService.make_request(url)

    @staticmethod
    def get_question() -> dict | None:
        url = f'/operation_roles/get'
        return BookingService.make_request(url)

    @staticmethod
    def get_reserved() -> dict | None:
        url = f'/operation_roles/get'
        return BookingService.make_request(url)

    @staticmethod
    def get_categories_dict(index) -> dict | None:
        url = f'/offices/getOperationsByIndex?index={int(index)}'
        return BookingService.make_request(url)

    @staticmethod
    def get_reserved_times(date: datetime) -> dict | None:
        url = f'/reserved/getByDate?date={date}'
        return BookingService.make_request(url)

    @staticmethod
    def get_booking_auth_hash(hash) -> dict | None:
        url = f'/booking_auth/hash/{hash}'
        return BookingService.make_request(url)

    @staticmethod
    def send_reserved(user_uuid, date, time, operation_id, operation_text, office_id):
        url = f'{BookingService.base_url}/reserved/add'

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {settings.AUTH_TOKEN}'
        }

        data = {
            "uuid": user_uuid,
            "reserved_date": f"{format_custom_date(date)}",
            "reserved_datetime": f"2024-10-19T{time}:00.000Z",
            "operation_id": operation_id,
            "operation_text": operation_text,
            "office_id": int(office_id)
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()

        else:
            print(f'Error from backend: {response.text}')
            return None

    @staticmethod
    def get_reserve_from_code(code):
        reserves = BookingService.get_reserve()

        for reserve in reserves['reserved']:
            if reserve['code'] == code:
                return reserve

        return None