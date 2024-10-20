from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from router.keyboards import get_categories_markup, get_days_keyboard_markup
from router.states import Form
from services.booking_service import BookingService
from storage.models.user import User

subcategories_page = Router()

def get_subcategory_info(data):
    subcategories_info = []
    if data.get("status") and data.get("operations"):
        for operation in data["operations"]:
            if operation.get("subcategories"):
                for subcategory in operation["subcategories"]:
                    subcategories_info.append({
                        "name": subcategory.get("name"),
                        "main_operation_id": subcategory.get("main_operation_id"),
                        "id": subcategory.get("id")
                    })
    return subcategories_info

@subcategories_page.message(Form.sub_categories)
async def subcategories(message: Message, state: FSMContext):
    match message.text:
        case 'Назад':
            index = User.get_by_id(message.chat.id)
            categories_data = BookingService.get_categories_dict(index)
            back_markup = get_categories_markup(categories_data)
            await message.answer(f'Выберите нужную Вам операцию: ', reply_markup=back_markup)
            await state.set_state(Form.menu)
            return

    markup = get_days_keyboard_markup()
    await state.set_state(Form.set_booking_day)

    index = User.get_by_id(message.chat.id).index
    categories = BookingService.get_categories_dict(index)
    subcategories = get_subcategory_info(categories)

    for subcategory in subcategories:
        if subcategory['name'] == message.text:
            await state.update_data(subcategory=message.text)
            await state.update_data(subcategory_id=subcategory['id'])

    await message.answer(f'Выберите удобный для вас день брони:', reply_markup=markup)