from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import time

from cost_calculations.scanner_tesseract.receipt_scanner import *
from buttons import *

wrong_company_name_price = []


class ScannerImage(StatesGroup):
    image_processing = State()
    output_user = State()


class ManualUserInput(StatesGroup):
    company_name = State()
    price = State()


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
        wrong_company_name_price.append([result_parsed()[1]])

        await message.answer('Введите название компании:')
        time.sleep(2)
        await message.answer('Пример: Два Гуся, 5 элемент, Спорт Мастер')

        await ManualUserInput.company_name.set()
    else:
        company_name, category_name, price = result_parsed()

        async with state.proxy() as result:
            result['company_name'] = company_name
            result['category_name'] = category_name
            result['price'] = price

        await message.answer(f"Название компании: {company_name}\nКатегория: {category_name}\nЦена покупок: {price}\nВсё верно?", reply_markup=check_user)

        await ScannerImage.output_user.set()


async def output_user_data(message: types.Message, state: FSMContext):
    text_user = message.text

    if text_user == 'Да':
        await message.answer('Данные сохранены вы их можете просмотреть на сайте', reply_markup=user_keyboard)

        wrong_company_name_price.clear()

        await state.finish()

    elif text_user == 'Неправильная цена':
        scan_info = await state.get_data()

        wrong_company_name_price.clear()
        wrong_company_name_price.append([scan_info['company_name'], scan_info['category_name'], scan_info['price']])

        await message.answer('Введите сумму покупок/покупок')

        await ManualUserInput.price.set()

    elif text_user == 'Неправильное название компании':
        scan_info = await state.get_data()

        wrong_company_name_price.clear()
        wrong_company_name_price.append([scan_info['company_name'], scan_info['category_name'], scan_info['price']])

        await message.answer('Введите название компании:')
        time.sleep(2)
        await message.answer('Пример: Два Гуся, 5 элемент, Спорт Мастер')

        await ManualUserInput.company_name.set()
    else:
        await message.answer('Я вас не понимаю, воспользуйтесь клавиатурой', reply_markup=check_user)


async def manual_input(message: types.Message):
    await message.answer('Введите название компании:')
    time.sleep(2)
    await message.answer('Пример: Два Гуся, 5 элемент, Спортмастер')

    await ManualUserInput.company_name.set()


async def get_company_name(message: types.Message, state: FSMContext):
    text_user = message.text
    with open(r'C:\Service_finance\cost_calculations\parser_spider\firmsdata\firmsdata\spiders\firms.csv',
              encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        name_street_firm = [row for row in csv_reader][1:]
    try:
        for name_firm, street, category in name_street_firm:
            if name_firm.lower() == text_user.lower():
                async with state.proxy() as name_company_category_company_price:
                    name_company_category_company_price['company_name'] = name_firm
                    name_company_category_company_price['category_name'] = category
                    if wrong_company_name_price:
                        name_company_category_company_price['price'] = wrong_company_name_price[0][-1]

                print(name_firm.lower())
                break
        else:
            raise Exception('Company name not found')

        if wrong_company_name_price:
            info_search = await state.get_data()
            await message.answer(
                f"Название компании: {info_search['company_name']}\nКатегория: {info_search['category_name']}\nЦена покупок: {wrong_company_name_price[0][-1]}\nВсё верно?",
                reply_markup=check_user)

            await ScannerImage.output_user.set()
        else:
            await message.answer('Введите сумму покупок/покупок')
            await ManualUserInput.price.set()

    except Exception as ex:
        print(ex)
        await message.answer('Название компании введено не верно, попробуйте отсканировать чек или ввести в ручную',
                             reply_markup=user_keyboard)
        await state.finish()


async def get_price(message: types.Message, state: FSMContext):
    text_user = message.text

    async with state.proxy() as name_company_category_company_price:
        name_company_category_company_price['price'] = text_user

    if wrong_company_name_price:
        await message.answer(
            f"Название компании: {wrong_company_name_price[0][0]}\nКатегория: {wrong_company_name_price[0][1]}\nЦена покупок: {text_user}\nВсё верно?",
            reply_markup=check_user)

        await ScannerImage.output_user.set()

    else:
        info_search = await state.get_data()
        await message.answer(
            f"Название компании: {info_search['company_name']}\nКатегория: {info_search['category_name']}\nЦена покупок: {text_user}\nВсё верно?",
            reply_markup=check_user)

        await ScannerImage.output_user.set()

