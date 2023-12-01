from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from cryptography.fernet import Fernet
import datetime
import time

from .db_postgres.postgres import Postgres
from .buttons_bot.buttons import *

from . import directory_english_characters

from dotenv import load_dotenv
import os

load_dotenv()

db = Postgres()

cipher_suite = Fernet(os.getenv('FERNET_KEY'))


class Registration(StatesGroup):
    login = State()
    password = State()
    save_status = State()


async def start(message: types.Message, state: FSMContext):
    await state.finish()
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


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer('Действие отменено', reply_markup=user_keyboard)


async def check_password_symbol(message):
    for symbol_password_users in message.text:
        for symbol in directory_english_characters.verification_symbol:
            if symbol == symbol_password_users:
                break
        else:
            continue
        break

    else:
        return False


async def login(message: types.Message, state: FSMContext):
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


async def viewing_login_password(message: types.Message):
    user_id = message.from_user.id
    info_user = db.select_table_registrations_user(user_id)
    login_user = info_user[0][0]
    password_user = info_user[0][1]

    decrypted_login = cipher_suite.decrypt(login_user)
    decrypted_password = cipher_suite.decrypt(password_user)

    await message.answer(f'Логин: {decrypted_login.decode()}\nПароль: {decrypted_password.decode()}', reply_markup=user_keyboard)

