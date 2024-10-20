from pyexpat.errors import messages

from aiogram import Router, F
from aiogram.enums import content_type
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, WebAppInfo

from router.pages.main_menu import main_menu_markup
from router.states import Form
from services.auth_service import AuthService
from storage.models.user import User

auth_page = Router()

auth_read_number_markup = ReplyKeyboardMarkup(
    keyboard=[
        # [
        #     KeyboardButton(text='Прикрепить привязанный номер', request_contact=True)
        # ],
        [
            KeyboardButton(text='Регистрация', web_app=WebAppInfo(url="https://enotgpt.ru/register"))
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True)

auth_read_code_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Изменить почту')
        ],
    ],
    resize_keyboard=True
)

@auth_page.message(Form.auth, F.text == 'Авторизоваться')
async def auth(message: Message, state: FSMContext):
    await state.set_state(Form.auth_read_number)
    await message.answer('Для авторизации потребуется ввести почту. \n\nЕсли вы не зарегистрированы, нажмите на кнопку ниже', reply_markup=auth_read_number_markup)

@auth_page.message(Form.auth_read_number)
async def auth_read_number(message: Message, state: FSMContext):
    number = None

    match message.content_type:
        case content_type.ContentType.CONTACT:
            email = message.contact.phone_number
        case content_type.ContentType.TEXT:
            email = message.text

    response = AuthService.request_code(email)
    await state.update_data(email=email)

    if response is None:
        await state.set_state(Form.auth)
        await message.answer('Почта не была найдена в системе.\n\nЗарегистрируйтесь или убедитесь в правильности введенных данных',
                             reply_markup=auth_read_number_markup)
        return

    await state.set_state(Form.auth_read_code)
    await state.update_data(code_id=response['code_id'])

    await message.answer('Введите код, отправленный в смс на указанную почту: ', reply_markup=auth_read_code_markup)

@auth_page.message(Form.auth_read_code, F.text == 'Изменить почту')
async def auth_read_code(message: Message, state: FSMContext):
    await state.set_state(Form.auth_read_number)
    await message.answer('Введите почту для авторизации: ', reply_markup=auth_read_number_markup)

@auth_page.message(Form.auth_read_code)
async def auth_read_code(message: Message, state: FSMContext):
    data = await state.get_data()
    code_id = data.get('code_id')
    code_value = ''.join(filter(str.isdigit, message.text))

    email = data.get('email')

    response = AuthService.auth(code_value, code_id, email)

    if response is None:
        await message.answer('Введен неверный код. Попробуйте снова')
        return

    access_token = response['access_token']

    User.create(telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                token=access_token,
                email=email)

    await state.set_state(Form.main_menu)
    await message.answer('Вы успешно авторизовались в боте', reply_markup=main_menu_markup)