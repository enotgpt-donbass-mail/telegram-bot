from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto

from router.redirects import redirect_to_main_menu
from router.states import Form
from services.booking_service import BookingService
from storage.models.user import User

hello_page = Router()

@hello_page.message(CommandStart(deep_link=True))
async def command_start(message: Message, state: FSMContext, command: CommandObject):
    try:
        User.get_by_id(message.from_user.id)
        await state.set_state(Form.menu)
        await redirect_to_main_menu(message)
    except Exception as e:
        args = command.args.split("__")

        auth_hash = args[0]
        hash_result = BookingService.get_booking_auth_hash(auth_hash)

        if hash_result is None or not hash_result['status']:
            await send_auth_instruction_message(message)
            return

        index = args[1]
        post = BookingService.get_post(index)

        if post is None or not post['status']:
            await send_auth_instruction_message(message)
            return

        office_id = post['office']['id']
        post_name = post['office']['name']

        User.create(telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    index=index,
                    office_id=office_id,
                    post_name=post_name)

        await state.set_state(Form.menu)
        await redirect_to_main_menu(message)

@hello_page.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    try:
        await state.set_state(Form.menu)
        await redirect_to_main_menu(message)
    except Exception as e:
        await send_auth_instruction_message(message)

async def send_auth_instruction_message(message):
    image_path = 'https://i.imgur.com/mbVXdUl.png'
    await message.answer(text='Авторизоваться в боте для электронной очереди можно на QR-коде, '
                              'который находится на терминале в отделениях "Почты Донбасса"')
    await message.answer_photo(photo=image_path)