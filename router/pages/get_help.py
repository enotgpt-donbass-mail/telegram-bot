from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from router.redirects import redirect_to_main_menu
from router.states import Form
from services.booking_service import BookingService

get_help_page = Router()

@get_help_page.message(Form.categories)
async def get_help(message: Message, state: FSMContext):
    match message.text:
        case 'Назад':
            await redirect_to_main_menu(message)
            await state.set_state(Form.menu)
            return

    question = message.text
    answer = BookingService.get_question(question)

    await message.answer(f'Агент поддержки: {answer}')