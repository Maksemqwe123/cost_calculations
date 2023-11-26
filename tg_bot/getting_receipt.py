from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import time

from cost_calculations.scanner_tesseract.receipt_scanner import *
from buttons import *


class ScannerImage(StatesGroup):
    image_processing = State()
    output_user = State()


async def scanner_receipt(message: types.Message):
    await message.answer('Отправьте нам фото чека')

    await ScannerImage.image_processing.set()


async def getting_image(message: types.Message, state: FSMContext):
    receipt = message.photo[-1]
    user_id = message.from_user.id

    path_save_image = fr'C:\Service_finance\cost_calculations\img_receipts\{user_id}.jpg'

    await receipt.download(destination_file=path_save_image)

    await message.answer('Подождите, идёт сканирование чека')

    image_data, payload = download_image(path_save_image)

    response = requests.post('https://api.ocr.space/parse/image', files={'image': image_data}, data=payload)

    result_parsed = OCR(response)

    if len(result_parsed()) == 1:
        await message.answer(result_parsed()[0])
        time.sleep(2)
        await message.answer('Попробуйте ввести название компании вручную или от сканируйте ещё раз',
                             reply_markup=user_keyboard)
        await state.finish()
    elif len(result_parsed()) == 2:
        await message.answer(f'{result_parsed()[0]}\nЦена покупки: {result_parsed()[1]}')

    else:
        company_name, category_name, price = result_parsed()

        await message.answer(f"Название компании: {company_name}\nКатегория: {category_name}\nЦена покупок: {price}\nВсё верно?", reply_markup=check_user)

        await ScannerImage.output_user.set()


async def output_user_data(message: types.Message, state: FSMContext):
    text_user = message.text

    if text_user == 'Да':
        pass
    elif text_user == 'Неправильная цена':
        pass
    elif text_user == 'Неправильное название компании':
        pass
    else:
        await message.answer('Я вас не понимаю, воспользуйтесь клавиатурой', reply_markup=check_user)
