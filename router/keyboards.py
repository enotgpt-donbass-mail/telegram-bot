import datetime

import pytz
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from services.booking_service import BookingService
from storage.models.user import User
from utils.category_formatter import format_category, reformat_category

def get_post_geo_inline_markup(location):
    url_button = InlineKeyboardButton(
        text='Показать на карте',
        url=f'https://yandex.ru/maps/?ll={location[0]}%2{location[1]}&z=18'
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[url_button]]
    )

    return keyboard

def get_cancel_inline_markup(callback_code):
    cancel_button = InlineKeyboardButton(
        text='Отменить место в очереди',
        callback_data=callback_code
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[cancel_button]]
    )

    return keyboard

def get_assessment_inline_markup(callback_code):
    star1 = InlineKeyboardButton(
        text='1 ⭐️',
        callback_data=f"assessment|1|{callback_code}"
    )

    star2 = InlineKeyboardButton(
        text='2 ⭐️',
        callback_data=f"assessment|2|{callback_code}"
    )

    star3 = InlineKeyboardButton(
        text='3 ⭐️',
        callback_data=f"assessment|2|{callback_code}"
    )

    star4 = InlineKeyboardButton(
        text='4 ⭐️',
        callback_data=f"assessment|2|{callback_code}"
    )

    star5 = InlineKeyboardButton(
        text='5 ⭐️',
        callback_data=f"assessment|2|{callback_code}"
    )

    cancel = InlineKeyboardButton(
        text='Воздержусь',
        callback_data=f"assessment|-1|{callback_code}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[star5, star4],
                         [star3, star2, star1],
                         [cancel]]
    )

    return keyboard

def get_my_reserved_markup(user_uuid):
    reserved = BookingService.get_reserve()
    my_reserved = []

    for reserve in reserved['reserved']:
        if reserve['uuid'] == user_uuid and reserve['status'] == -10:
            my_reserved.append(reserve)

    buttons = []

    for reserve in my_reserved:
        button = InlineKeyboardButton(
            text=f'{reserve['operation_text']} (Код: {reserve['code']}',
            callback_data=f'delete|{reserve['id']}'
        )
        buttons.append(button)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f'{reserve["operation_text"]} (Код: {reserve["code"]})',
                callback_data=f'delete|{reserve["id"]}'
            )] for reserve in my_reserved
        ]
    )

    return keyboard

def get_back_markup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Назад")
            ]
        ],
        resize_keyboard=True)

def get_geo_markup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Прислать гео-локацию", request_location=True),
                KeyboardButton(text="Назад")
            ]
        ],
        resize_keyboard=True)

def get_switch_index_markup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📋 Выбрать отделение по индексу")
            ],
            [
                KeyboardButton(text="📍 Выбрать ближайшее отделение", request_location=True)
            ],
            [
                KeyboardButton(text="🗂 Выбрать ближайшее отделение по услуге")
            ],
            [
                KeyboardButton(text="Назад")
            ],
        ],
        )

def get_main_menu_markup(user_id) -> ReplyKeyboardMarkup:
    user = User.get_by_id(user_id)

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"📫 Выбранная почта: {user.post_name}")
            ],
            [
                KeyboardButton(text="📦 Записаться в очередь")
            ],
            [
                KeyboardButton(text="👤 Мои записи"),
                KeyboardButton(text="🔗 Изменить отделение"),
                # KeyboardButton(text="🔍 Помощь")
            ],
        ],
        resize_keyboard=True)

def get_categories_markup(categories_json) -> ReplyKeyboardMarkup:
    """Преобразует JSON-данные с операциями в ReplyKeyboardMarkup."""

    buttons = []

    for operation in categories_json['operations']:
        main_button = KeyboardButton(text=format_category(operation['name']))
        buttons.append(main_button)

    back = KeyboardButton(text='Назад')
    buttons.append(back)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [button] for button in buttons
        ],
        resize_keyboard=True
    )

    return keyboard

def get_subcategories_markup(categories_json, category) -> ReplyKeyboardMarkup:
    """Преобразует JSON-данные с операциями в ReplyKeyboardMarkup."""

    buttons = []

    for operation in categories_json['operations']:
        if operation['name'] == reformat_category(category):
            if operation['subcategories']:
                for subcategory in operation['subcategories']:
                    button = KeyboardButton(text=subcategory['name'])
                    buttons.append(button)

    if len(buttons) == 0:
        return None

    back = KeyboardButton(text='Назад')
    buttons.append(back)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [button] for button in buttons
        ],
        resize_keyboard=True
    )

    return keyboard

def get_days_keyboard_markup() -> ReplyKeyboardMarkup:
    today = datetime.date.today()
    dates = [today + datetime.timedelta(days=i) for i in range(7)]

    months = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня',
        7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"Сегодня"),
                KeyboardButton(text=f"Завтра"),
                KeyboardButton(text=f"Послезавтра")
            ],
            [
                KeyboardButton(text=f"{dates[3].day} {months[dates[3].month]}"),
                KeyboardButton(text=f"{dates[4].day} {months[dates[4].month]}"),
            ],
            [
                KeyboardButton(text=f"{dates[5].day} {months[dates[5].month]}"),
                KeyboardButton(text=f"{dates[6].day} {months[dates[6].month]}"),
            ],
            [
                KeyboardButton(text="Назад")
            ]
        ],
        resize_keyboard=True)

def get_times_keyboard_markup(reserved_times: dict, date, office_id) -> ReplyKeyboardMarkup:
    now = datetime.datetime.now(pytz.timezone("Europe/Moscow"))
    target_time = datetime.datetime.combine(now.date(), datetime.time(17, 30), tzinfo=now.tzinfo)

    buttons = []
    time_slots = []

    if datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").date() != datetime.date.today():
        current_time = now.replace(hour=9, minute=00, second=0, microsecond=0)
    else:
        print('today')
        current_time = now.replace(second=0, microsecond=0)

    while current_time <= target_time:
        current_time_minute = (current_time.minute // 15) * 15
        current_time = current_time.replace(minute=current_time_minute, second=0, microsecond=0)

        for reserved in reserved_times['reserved']:
            reserved_datetime = datetime.datetime.strptime(reserved['reserved_datetime'], "%Y-%m-%dT%H:%M:%S")

            if reserved_datetime.hour == current_time.hour and reserved_datetime.minute == current_time.minute and office_id == reserved['office_id']:
                continue

        time_slots.append(current_time.strftime("%H:%M"))
        current_time += datetime.timedelta(minutes=15)

    for slot in time_slots:
        button = KeyboardButton(text=slot)
        buttons.append(button)

    back = KeyboardButton(text='Назад')
    buttons.append(back)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [button] for button in buttons
        ],
        resize_keyboard=True
    )

    return keyboard

def get_booking_confirm_markup() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Изменить время брони"),
                KeyboardButton(text="Все в порядке")
            ],
        ],
        resize_keyboard=True)