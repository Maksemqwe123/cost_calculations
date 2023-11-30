from register_user import *
from getting_info_receipt import *

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(cancel, commands='cancel', state='*')


def register_handlers_user_register(dp: Dispatcher):
    dp.register_message_handler(login, state=Registration.login)
    dp.register_message_handler(password, state=Registration.password)
    dp.register_message_handler(save_login_password, state=Registration.save_status)
    dp.register_message_handler(viewing_login_password, Text(equals='Посмотреть логин и пароль'))


def register_handlers_getting_receipt(dp: Dispatcher):
    dp.register_message_handler(scanner_receipt, Text(equals='Отсканировать чек', ignore_case=True))
    dp.register_message_handler(getting_image, content_types=types.ContentType.PHOTO, state=ScannerImage.image_processing)
    dp.register_message_handler(output_user_data, state=ScannerImage.output_user)
    dp.register_message_handler(manual_input, Text(equals='Внести вручную'))
    dp.register_message_handler(get_company_name, state=ManualUserInput.company_name)
    dp.register_message_handler(get_price, state=ManualUserInput.price)

