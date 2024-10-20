from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from router.keyboards import get_categories_markup, get_days_keyboard_markup, get_times_keyboard_markup
from router.states import Form
from services.booking_service import BookingService
from storage.models.user import User
from utils.date_formatter import format_custom_date

set_booking_day_page = Router()

@set_booking_day_page.message(Form.set_booking_day)
async def set_booking_day(message: Message, state: FSMContext):
    match message.text:
        case 'Назад':
            index = User.get_by_id(message.from_user.id).index
            categories_data = BookingService.get_categories_dict(index)
            back_markup = get_categories_markup(categories_data)
            await message.answer(f'Выберите нужную Вам операцию: ', reply_markup=back_markup)
            await state.set_state(Form.menu)
            return

    reserved_times = BookingService.get_reserved_times(format_custom_date(message.text))
    office_id = User.get_by_id(message.from_user.id).office_id
    markup = get_times_keyboard_markup(reserved_times, format_custom_date(message.text), office_id)
    await state.set_state(Form.set_booking_time)
    await state.update_data(date=message.text)

    await message.answer(f'Выберите удобное для вас время брони:', reply_markup=markup)