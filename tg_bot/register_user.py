from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from cryptography.fernet import Fernet
import datetime
import time

from cost_calculations.db_postgres.postgres import Postgres
from cost_calculations.config.config_reader import load_config
from buttons import *

from directory_english_characters import verification_symbol

path_config_ini = r'C:\Service_finance\cost_calculations\config\config.ini'

db = Postgres()

fernet_key = load_config(path_config_ini).text_encryption.fernet_key


class Registration(StatesGroup):
    login = State()
    password = State()
    save_status = State()


async def start(message: types.Message):
    user_id = message.from_user.id
    if db.select_table_registrations_user(user_id):
        await message.answer('И снова привет, что вы хотите сделать?', reply_markup=user_keyboard)
    else:
        await message.answer('Привет, я бот, который сканирует чеки и записывает твои расходы')
        time.sleep(1)
        await message.answer('Мне нужно тебя запомнить, придумай себе логин и пароль')
        time.sleep(1)

        await message.answer('Введите логин')

        await Registration.login.set()


async def check_password_symbol(message):
    for symbol_password_users in message.text:
        for symbol in verification_symbol:
            if symbol == symbol_password_users:
                break
        else:
            continue
        break

    else:
        return False


async def login(message: types.Message, state: FSMContext):
    cipher_suite = Fernet(fernet_key)
    # Преобразование строки в байтовый формат
    plaintext_bytes = message.text.encode()
    # Шифрование строки
    ciphertext = cipher_suite.encrypt(plaintext_bytes)

    if db.check_login_user(ciphertext.decode()):
        await message.answer('Такой логин уже есть')

        await message.answer('Введите логин')
        await Registration.login.set()

    else:
        await message.answer('секунду')

        if message.text.find(' ') != -1:
            await message.answer('В логине не должно содержаться пробелов')

            await message.answer('Введите логин')
            await Registration.login.set()

        else:
            check_password = await check_password_symbol(message)
            if check_password is None:
                user_login_password = await state.get_data()
                if 'user_password' in user_login_password.keys():
                    await message.answer(
                        f'login: {user_login_password["user_login"]}\npassword: {user_login_password["user_password"]}\nВсё верно?',
                        reply_markup=confirmation_login_password
                    )
                    await Registration.save_status.set()
                else:
                    await message.answer('Придумайте пароль')
                    await state.update_data(user_login=message.text)
                    await Registration.password.set()

            else:
                await message.answer('Логин должен состоять из латинских букв')

                await message.answer('Введите логин')
                await Registration.login.set()


async def password(message: types.Message, state: FSMContext):
    print(message.text)
    user_login_password = await state.get_data()
    if "user_password" in user_login_password.keys():
        if user_login_password['user_password'] == message.text:
            await message.answer(
                f'login: {user_login_password["user_login"]}\npassword: {user_login_password["user_password"]}\nВсё верно?',
                reply_markup=confirmation_login_password
            )
            await Registration.save_status.set()

        else:
            await message.answer('Пароли не совпадают, попробуйте заново')
            async with state.proxy() as user_login_password:
                user_login_password.pop('user_password')

            await message.answer('Введите пароль')
            await Registration.password.set()

    else:
        await state.update_data(user_password=message.text)
        await message.delete()

        await message.answer('Повторите пароль')

        await Registration.password.set()


async def save_login_password(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        user_login_password = await state.get_data()

        cipher_suite = Fernet(fernet_key)

        user_login_bytes = str(user_login_password['user_login']).encode()
        cipher_login = cipher_suite.encrypt(user_login_bytes)

        user_password_bytes = str(user_login_password['user_password']).encode()
        cipher_password = cipher_suite.encrypt(user_password_bytes)

        dttm_now = datetime.datetime.now()

        db.insert_table_registrations_user(
            str(message.from_user.id), str(message.from_user.username), cipher_login.decode(), cipher_password.decode(), str(dttm_now)
        )
        await message.answer('Поздравляю вы прошли регистрацию', reply_markup=user_keyboard)
        await state.finish()

    elif message.text == 'Изменить логин':
        async with state.proxy() as user_login_password:
            user_login_password.pop('user_login')
        await message.answer('Введите новый логин')

        await Registration.login.set()

    elif message.text == 'Изменить пароль':
        async with state.proxy() as user_login_password:
            user_login_password.pop('user_password')
        await message.answer('Введите новый пароль')

        await Registration.password.set()

    else:
        await message.answer('Я не понимаю вас, воспользуетесь пожалуйста клавиатурой')
        await Registration.save_status.set()
