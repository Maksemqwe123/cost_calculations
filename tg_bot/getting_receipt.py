from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class ScannerImage(StatesGroup):
    image_processing = State()


async def scanner_receipt(message: types.Message):
    await message.answer('Отправьте нам фото чека')

    await ScannerImage.image_processing.set()


async def getting_image(message: types.Message, state: FSMContext):
    print(message.photo)
    receipt = message.photo[-1]

    await receipt.download(destination=r'C:\Service_finance\cost_calculations\img_receipts')

