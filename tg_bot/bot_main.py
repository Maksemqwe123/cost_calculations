from aiogram import Bot
from aiogram.utils import executor

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from register_handlers_main import *
from cost_calculations.config.config_reader import load_config

path_config_ini = r'C:\Service_finance\cost_calculations\config\config.ini'

storage = MemoryStorage()

bot = Bot(load_config(path_config_ini).tg_bot.token)
dp = Dispatcher(bot, storage=storage)


if __name__ == '__main__':
    register_handlers_commands(dp)
    register_handlers_user_register(dp)
    register_handlers_getting_receipt(dp)

    executor.start_polling(dp, skip_updates=True)
