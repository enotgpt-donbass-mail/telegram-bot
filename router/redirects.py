from router.keyboards import get_main_menu_markup, get_switch_index_markup


async def redirect_to_main_menu(message):
    await message.answer('📫 Главное меню', reply_markup=get_main_menu_markup(message.from_user.id))

async def redirect_to_change_index(message):
    await message.answer('Выберите вариант смены почтового отделения: ', reply_markup=get_switch_index_markup())

async def redirect_to_error(message):
    await message.answer('Возникла ошибка. Повторите попытку позже', reply_markup=get_main_menu_markup(message.from_user.id))

