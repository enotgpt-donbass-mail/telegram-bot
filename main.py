import asyncio
import logging
import threading
from datetime import datetime

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from router.debug_commands import debug_notify_before_hour
from router.pages.booking_confirm import booking_confirm_page
from router.pages.categories import categories_page
from router.pages.get_help import get_help_page
from router.pages.hello import hello_page
from router.pages.main_menu import main_menu_page
from router.pages.set_booking_day import set_booking_day_page
from router.pages.set_booking_time import set_booking_time_page
from router.pages.subcategories import subcategories_page
from router.pages.switch_index import switch_index_page
from services.notifications_worker import NotificationsWorker
from settings import TELEGRAM_TOKEN
from storage.models.user import User
from storage.storage import database

bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

file_log = logging.FileHandler(f'./logs/log {datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log')
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out),
                    format='[%(asctime)s | %(levelname)s]: %(message)s',
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.INFO)

def pages_dispatcher():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router=hello_page)
    dp.include_router(router=main_menu_page)
    dp.include_router(router=switch_index_page)
    dp.include_router(router=categories_page)
    dp.include_router(router=subcategories_page)
    dp.include_router(router=set_booking_day_page)
    dp.include_router(router=set_booking_time_page)
    dp.include_router(router=booking_confirm_page)
    dp.include_router(router=get_help_page)

    # Register debug commands
    dp.message.register(debug_notify_before_hour, Command(commands=["debug_notify_before_hour"]))

    return dp

def create_tables():
    with database:
        database.create_tables([User])

def start_workers():
    notification_worker = NotificationsWorker()
    # notification_worker_thread = threading.Thread(target=notification_worker.run())
    # notification_worker_thread.start()

async def main():
    logging.info('Bot started')

    create_tables()

    start_workers()

    dp = pages_dispatcher()
    await dp.start_polling(bot)

asyncio.run(main())