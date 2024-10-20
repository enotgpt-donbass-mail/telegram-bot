from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from router.keyboards import get_times_keyboard_markup
from router.redirects import redirect_to_main_menu
from router.states import Form
from services.booking_service import BookingService
from storage.models.user import User
from utils.date_formatter import format_custom_date

booking_confirm_page = Router()

@booking_confirm_page.message(Form.confirm_booking)
async def categories(message: Message, state: FSMContext):
    match message.text:
        case 'Изменить время брони':
            reserved_times = BookingService.get_reserved_times(format_custom_date(message.text))
            data = await state.get_data()
            date = data.get('date')
            office_id = User.get_by_id(message.from_user.id).office_id
            back_markup = get_times_keyboard_markup(reserved_times, date, office_id)
            await state.set_state(Form.set_booking_time)
            await message.answer(f'Выберите удобное для вас время брони:', reply_markup=back_markup)
            return

        case 'Все в порядке':
            user = User.get_by_id(message.from_user.id)
            data = await state.get_data()
            time = data.get('time')
            date = data.get('date')
            subcategory = data.get('subcategory')
            subcategory_id = data.get('subcategory_id')
            result = BookingService.send_reserved(user_uuid=user.login, office_id=user.office_id, date=date, time=time, operation_text=subcategory, operation_id=subcategory_id)
            await message.answer(f'Ваш код брони - <b>{result['reserved']['code']}</b>. Введите его на терминале и получите талон. После заданного времени, бронь будет аннулирована.\n\nОтказаться от брони можно в разделе "Мои брони"', parse_mode=ParseMode.HTML)
            await state.set_state(Form.menu)
            await redirect_to_main_menu(message)
            return