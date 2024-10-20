from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from router.keyboards import get_days_keyboard_markup, get_booking_confirm_markup
from router.states import Form
from storage.models.user import User

set_booking_time_page = Router()

@set_booking_time_page.message(Form.set_booking_time)
async def set_booking_day(message: Message, state: FSMContext):
    match message.text:
        case 'Назад':
            markup = get_days_keyboard_markup()
            await message.answer(f'Выберите удобный для вас день брони:', reply_markup=markup)
            await state.set_state(Form.set_booking_day)
            return

    markup = get_booking_confirm_markup()
    await state.set_state(Form.confirm_booking)

    await state.update_data(time=message.text)

    # формируем результат
    data = await state.get_data()
    post = User.get_by_id(message.from_user.id).post_name

    result = f'<blockquote><b>Почтовое отделение:</b> {post}\n\n<b>Операция:</b> {data.get('subcategory')} ({data.get('category')})\n\n<b>Время:</b> {data.get('date')} в {message.text}</blockquote>'

    await message.answer(f'Подтвердите сформированную бронь на очередь:\n{result}', reply_markup=markup, parse_mode=ParseMode.HTML)