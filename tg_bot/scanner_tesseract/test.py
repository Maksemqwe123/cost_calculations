# text = """006'
# ОмеЈЛЬ
# Подненнвм фонд llT0
# РУП ИПО ”5елоруснеФть”
# код унп: 400051902
# Документ
# ПЛАТЕЖНЬш ДОКУМЕНТ
# Чек продажи 239/417
# 3718832 09.10.2023
# --—-#
# АИ-92-К5 Евро ТРК 2)
# #ндс
# Итого к оплате
# т.ч. ндс
# Оплачено (Безнал)
# 328219761220
# #Вплата прп-здказе:
# 13,56
# 13,56
# 13,56
# жарта *Заправка*
# #начислено бонусов за покупку:
# 6#
# (ассир Буханченко А.А,
# гон в скко/3Н скю: 110139228/300127755
# 09-10-2023
# для получения 3СЧФ испош зуйје
# vata!b.beloil .by
# """
#
#
# # from autocorrect import Speller
# #
# # spell = Speller('ru')
# # # fixed_text = spell(text)
# # # print(fixed_text)
# #
# #
# # from textblob import TextBlob
# #
# # blob = TextBlob(text)
# # fixed_text = str(blob.correct())
# # print(fixed_text)
#
#
#
#
#
import pytesseract

from PIL import Image, ImageFilter, ImageEnhance

path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image = Image.open(r'C:\Service_finance\img_receipts\8.jpg')

pytesseract.pytesseract.tesseract_cmd = path

# Примените фильтр для улучшения резкости
sharpened_image = image.filter(ImageFilter.SHARPEN)

white_black_image = sharpened_image.convert('L')

sharpened_image_1 = white_black_image.filter(ImageFilter.SHARPEN)

# filtered_image = image.filter(ImageFilter.FIND_EDGES)

# # Улучшите контрастность
# enhancer_contrast = ImageEnhance.Contrast(sharpened_image)
# enhanced_image_contrast = enhancer_contrast.enhance(1.1)
#
# # Улучшите яркость
# enhancer_brightness = ImageEnhance.Brightness(enhanced_image_contrast)
# enhanced_image_brightness = enhancer_brightness.enhance(1.2)
# sharpened_image.show()
def filter_colors(pixel):
    if pixel < 128:
        return 0  # Черный цвет
    else:
        return 255  # Белый цвет

filtered_image = sharpened_image_1.point(filter_colors)  # Применение фильтра к каждому пикселю изображения
# filtered_image_1 = sharpened_image_1.convert('1')
#
# sharpened_image_2 = filtered_image_1.filter(ImageFilter.SHARPEN)


# filtered_image.show()

# Увеличьте контрастность
sharpened_image_1.show()

text_1 = pytesseract.image_to_string(sharpened_image_1, lang='rus')

# enhanced_image = sharpened_image.enhance(фактор_контрастности)

print(text_1)
#
# # print('\n\n\n\n\n\n\n\n')
#
#
#


import difflib

word = "lim"
comparison_word = "limon"

similarity = difflib.SequenceMatcher(None, comparison_word, word).ratio() * 100

print(similarity)
if similarity >= 85:
    print(word)

# new_name_firm = ' '.join(word.capitalize() for word in name_firm.replace('”', '').split())
# if new_sentence.find(new_name_firm) != -1:
#     if new_name_firm != 'A1' and new_name_firm != 'Мир' and new_name_firm != 'Туалет':
#         print(new_name_firm)
#         break