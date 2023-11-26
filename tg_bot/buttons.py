from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

confirmation_login_password = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Да')
).add(
    KeyboardButton('Изменить пароль'),
    KeyboardButton('Изменить логин')
)


user_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Посмотреть логин и пароль')
).add(
    KeyboardButton('Отсканировать чек'),
    KeyboardButton('Внести вручную')
)

check_user = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Да')
).add(
    KeyboardButton('Неправильная цена')
).add(
    KeyboardButton('Неправильное название компании')
)
