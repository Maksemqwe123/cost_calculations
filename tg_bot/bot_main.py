from aiogram import Bot
from aiogram.utils import executor

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from register_handlers_main import *

from dotenv import load_dotenv
import os

load_dotenv()

storage = MemoryStorage()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)


if __name__ == '__main__':
    register_handlers_commands(dp)
    register_handlers_user_register(dp)
    register_handlers_getting_receipt(dp)

    executor.start_polling(dp, skip_updates=True)
