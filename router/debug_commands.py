from aiogram import types

from services.booking_service import BookingService
from services.notifications_worker import send_message_before_15_mins
from storage.models.user import User

async def debug_notify_before_hour(message: types.Message):
    try:
        code = int(message.get_args())
        if code <= 0:
            await message.reply("Please provide a positive code")
            return

        user = User.get_by_id(message.from_user.id)

        reserve = BookingService.get_reserve_from_code(code)

        if reserve is None:
            await message.reply("Code is not found in db")

        send_message_before_15_mins(user.uuid, code, reserve['reserved_datetime'].strftime("H:%M"), reserve['operation_text'])
        return

    except Exception as e:
        await message.reply("Debug error")