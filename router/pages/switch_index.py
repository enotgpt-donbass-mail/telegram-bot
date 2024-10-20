import types

from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from router.keyboards import get_main_menu_markup, get_back_markup, get_categories_markup, get_subcategories_markup, \
    get_geo_markup
from router.pages.subcategories import get_subcategory_info
from router.redirects import redirect_to_main_menu, redirect_to_change_index
from router.states import Form
from services.booking_service import BookingService
from storage.models.user import User
from utils.category_formatter import reformat_category
from utils.geolocation import get_closest_location

switch_index_page = Router()

@switch_index_page.message(Form.switch_index, F.text == '📋 Выбрать отделение по индексу')
async def switch_by_index(message: Message, state: FSMContext):
    await state.set_state(Form.switch_index_read_index)
    await message.answer(f'Введите индекс почтового отделения: ', reply_markup=get_back_markup())

@switch_index_page.message(Form.switch_index, F.text == '🗂 Выбрать ближайшее отделение по услуге')
async def switch_by_index(message: Message, state: FSMContext):
    await state.set_state(Form.switch_index_closest_category)
    categories_data = BookingService.get_operations()
    markup = get_categories_markup(categories_data)
    await message.answer(f'Выберите категорию услуги: ', reply_markup=markup)

@switch_index_page.message(Form.switch_index_closest_category)
async def switch_by_index_closest_category(message: Message, state: FSMContext):
    match message.text:
        case 'Назад':
            categories_data = BookingService.get_operations()
            back_markup = get_categories_markup(categories_data)
            await message.answer(f'Выберите категорию услуги: ', reply_markup=back_markup)
            await state.set_state(Form.menu)
            return

    await state.set_state(Form.switch_index_closest_subcategory)
    categories_data = BookingService.get_operations()
    markup = get_subcategories_markup(categories_data, reformat_category(message.text))
    await message.answer(f'Выберите операцию: ', reply_markup=markup)

@switch_index_page.message(Form.switch_index_closest_subcategory)
async def switch_by_index_closest_subcategory(message: Message, state: FSMContext):
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude

        data = await state.get_data()
        subcategory_id = data.get('subcategory_switch_id')

        posts = BookingService.get_post_by_subcategory_id(subcategory_id)['offices']

        closest_post = get_closest_location(latitude, longitude, posts)
        await set_new_post(closest_post['index'], message)
        await state.set_state(Form.menu)
        return

    match message.text:
        case 'Назад':
            categories_data = BookingService.get_operations()
            back_markup = get_categories_markup(categories_data)
            await message.answer(f'Выберите операцию: ', reply_markup=back_markup)
            await state.set_state(Form.switch_index_closest_category)
            return

    categories = BookingService.get_operations()
    subcategories = get_subcategory_info(categories)

    for subcategory in subcategories:
        if subcategory['name'] == message.text:
            subcategory_id = subcategory['id']

            posts = BookingService.get_post_by_subcategory_id(subcategory_id)

            if posts is None or not posts['status']:
                categories_data = BookingService.get_operations()
                back_markup = get_categories_markup(categories_data)
                await message.answer(f'Отделений с такой операций в данных момент нет. Выберите другую операцию: ', reply_markup=back_markup)
                await state.set_state(Form.switch_index_closest_category)
                return

            await state.update_data(subcategory_switch_id=subcategory_id)
            await message.answer('Укажите свою гео-локацию, чтобы определить ближайшее к Вам отделение', reply_markup=get_geo_markup())
            return

    categories_data = BookingService.get_operations()
    back_markup = get_categories_markup(categories_data)
    await message.answer(f'Отделений с такой операций в данных момент нет. Выберите другую операцию: ',
                         reply_markup=back_markup)
    await state.set_state(Form.switch_index_closest_category)
    return


@switch_index_page.message(Form.switch_index_read_index)
async def switch_by_index_read(message: Message, state: FSMContext):
    match message.text:
        case 'Назад':
            await state.set_state(Form.switch_index)
            await redirect_to_change_index(message)
            return

    try:
        await set_new_post(message.text, message)
        await state.set_state(Form.menu)
        return

    except Exception as e:
        await message.answer(f'Отделение с таким индексом не найдено. Проверьте корректность введенных данных')

@switch_index_page.message(Form.switch_index)
async def handler(message: Message, state: FSMContext):

    # '📍 Выбрать ближайшее отделение'
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude

        posts = BookingService.get_posts()['offices']

        closest_post = get_closest_location(latitude, longitude, posts)
        await state.set_state(Form.menu)
        await set_new_post(closest_post['index'], message)
        return

    match message.text:
        case 'Назад':
            await redirect_to_main_menu(message)
            await state.set_state(Form.menu)
            return

async def set_new_post(index, message):
    post = BookingService.get_post(index)

    post_name = post['office']['name']
    index = post['office']['index']
    office_id = post['office']['id']

    user = User.get_by_id(message.from_user.id)
    user.post_name = post_name
    user.index = index
    user.office_id = office_id
    user.save()

    await message.answer(f'Почтовое отделение было изменено на отделение <b>"{post_name}"</b>',
                         reply_markup=get_main_menu_markup(message.from_user.id), parse_mode='HTML')