from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from router.keyboards import get_subcategories_markup
from router.redirects import redirect_to_main_menu
from router.states import Form
from services.booking_service import BookingService
from storage.models.user import User
from utils.category_formatter import reformat_category

categories_page = Router()

@categories_page.message(Form.categories)
async def categories(message: Message, state: FSMContext):
    match message.text:
        case 'Назад':
            await redirect_to_main_menu(message)
            await state.set_state(Form.menu)
            return

    index = User.get_by_id(message.from_user.id).index
    categories_data = BookingService.get_categories_dict(index)

    await state.update_data(category=reformat_category(message.text))

    await state.set_state(Form.sub_categories)
    markup = get_subcategories_markup(categories_data, message.text)

    if markup is None:
        await message.answer(f'Введена некорректная услуга, выберите услугу из списка')
        return

    await message.answer(f'Выберите нужную Вам операцию: ', reply_markup=markup)