from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from router.keyboards import get_categories_markup, get_post_geo_inline_markup, get_back_markup, get_my_reserved_markup
from router.redirects import redirect_to_error, redirect_to_change_index
from router.states import Form
from services.booking_service import BookingService
from storage.models.user import User

main_menu_page = Router()

@main_menu_page.message(Form.menu, F.text == '📦 Записаться в очередь')
async def show_main_menu(message: Message, state: FSMContext):
    index = User.get_by_id(message.from_user.id).index
    categories_data = BookingService.get_categories_dict(index)

    if categories_data is None:
        await redirect_to_error(message)
        return

    await state.set_state(Form.categories)
    await message.answer(f'Выберите нужную Вам категорию: ', reply_markup=get_categories_markup(categories_data))

@main_menu_page.message(Form.menu, F.text == '👤 Мои записи')
async def show_bookings(message: Message, state: FSMContext):
    user_uuid = User.get_by_id(message.from_user.id).login
    markup = get_my_reserved_markup(user_uuid)
    await state.set_state(Form.get_booking)
    await message.answer('Ваши записи: (нажмите на неё, чтобы отменить)', reply_markup=markup)

@main_menu_page.message(Form.menu, F.text == '🔗 Изменить отделение')
async def show_main_menu(message: Message, state: FSMContext):
    await state.set_state(Form.switch_index)
    await redirect_to_change_index(message)

@main_menu_page.message(Form.menu, F.text.startswith('📫 Выбранная почта:'))
async def show_main_menu(message: Message, state: FSMContext):
    index = User.get_by_id(message.from_user.id).index
    post = BookingService.get_post(index)

    operating_windows_length = len(post["office"]["operating_windows"])

    response = (f'<b>Выбранная почта: </b>\n\n<b>Название:</b> {post['office']['name']}\n'
               f'<b>Адрес:</b> {post['office']['place']}\n<b>Индекс:</b> {post['office']['index']}\n'
               f'<b>Окон обслуживания:</b> {operating_windows_length}')
    await message.answer(response, parse_mode=ParseMode.HTML, reply_markup=get_post_geo_inline_markup(post['office']['coordinates']))

@main_menu_page.message(Form.menu, F.text == '🔍 Помощь')
async def show_main_menu(message: Message, state: FSMContext):
    await state.set_state(Form.get_help)
    await message.answer('<b>Задайте ваш вопрос: </b>', parse_mode=ParseMode.HTML, reply_markup=get_back_markup())