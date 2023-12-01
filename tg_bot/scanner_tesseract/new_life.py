# import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
#
# path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#
# image = Image.open(r'C:\Service_finance\img_receipts\1.jpg')
#
# pytesseract.pytesseract.tesseract_cmd = path
#
# # Примените фильтр для улучшения резкости
# sharpened_image = image.filter(ImageFilter.SHARPEN)
#
# white_black_image = sharpened_image.convert('L')
#
# sharpened_image_1 = white_black_image.filter(ImageFilter.SHARPEN)
#
# # filtered_image = image.filter(ImageFilter.FIND_EDGES)
#
# # # Улучшите контрастность
# # enhancer_contrast = ImageEnhance.Contrast(sharpened_image)
# # enhanced_image_contrast = enhancer_contrast.enhance(1.1)
# #
# # # Улучшите яркость
# # enhancer_brightness = ImageEnhance.Brightness(enhanced_image_contrast)
# # enhanced_image_brightness = enhancer_brightness.enhance(1.2)
# # sharpened_image.show()
# def filter_colors(pixel):
#     if pixel < 128:
#         return 0  # Черный цвет
#     else:
#         return 255  # Белый цвет
#
# filtered_image = sharpened_image_1.point(filter_colors)  # Применение фильтра к каждому пикселю изображения
# # filtered_image_1 = sharpened_image_1.convert('1')
# #
# # sharpened_image_2 = filtered_image_1.filter(ImageFilter.SHARPEN)
#
#
# # filtered_image.show()
#
# # Увеличьте контрастность
# # sharpened_image.show()
#
# text = pytesseract.image_to_string(sharpened_image_1, lang='rus')
#
# # enhanced_image = sharpened_image.enhance(фактор_контрастности)
#
# print(text)
#
# # print('\n\n\n\n\n\n\n\n')


import cv2

import matplotlib.pyplot as plt

image_1 = cv2.imread('/cost_calculations/img_receipts\photo_2023-10-25_20-11-16.jpg')
gray_image = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)
# plt.axis('off')
cv2.imshow('Изображение', image_1)
# plt.show()


path_ = r'C:\Users\makce\Downloads\lite-model_east-text-detector_dr_1.tflite'


import cv2
import numpy as np
import tensorflow as tf
import pytesseract

# # Загрузка модели EAST
# model_path = r'C:\Users\makce\Downloads\lite-model_east-text-detector_dr_1.tflite'
# net = cv2.dnn.readNet(model_path)
#
# # Загрузка изображения
# image_path = image_1
# image = cv2.imread(image_path)
#
# # Предобработка изображения
# blob = cv2.dnn.blobFromImage(image, 1.0, (320, 320), (123.68, 116.78, 103.94), True, False)
#
# # Проход через сеть
# net.setInput(blob)
# output = net.forward()
#
# # Обработка результатов
# scores = output[0, 0, :, 2]
# geometry = output[0, 0, :, 3:7]
# indices = np.where(scores > 0.5)
#
# # Извлечение координат и ориентации текста
# boxes = []
# for i in indices[0]:
#     angle = geometry[i, 1]
#     x, y, w, h = geometry[i, 3] * 4, geometry[i, 4] * 4, geometry[i, 5] * 4, geometry[i, 6] * 4
#     boxes.append((x, y, w, h, angle))
#
# # Распознавание текста
# for (x, y, w, h, angle) in boxes:
#     # Выделение региона с текстом
#     roi = image[int(y):int(y + h), int(x):int(x + w)]
#
#     # Преобразование региона с текстом в оттенки серого
#     gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#
#     # Применение порогового значения для улучшения контраста
#     _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#
#     # Применение метода распознавания текста (например, Tesseract)
#     text = pytesseract.image_to_string(threshold, lang='rus')
#
#     # Вывод распознанного текста
#     print("Распознанный текст:", text)
#
# # Вывод результатов
# cv2.imshow('Text Detection', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Загрузка модели EAST
model = tf.lite.Interpreter(model_path=path_)
model.allocate_tensors()

# Загрузка изображения
image = cv2.imread(r'/cost_calculations/img_receipts\photo_2023-10-25_20-11-16.jpg')

gray_image_1 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Предобработка изображения
image = cv2.resize(gray_image_1, (320, 320))
image = np.reshape(image, (1, 320, 320, 3))

image = image.astype(np.float32)
image = image / 255.0
# image = np.expand_dims(gray_image_1, axis=0)
print(image.shape)





# Выполнение распознавания текста
input_details = model.get_input_details()
output_details = model.get_output_details()
# print(input_details)

model.set_tensor(input_details[0]['index'], image)
model.invoke()

output_data = model.get_tensor(output_details[0]['index'])
geometry = model.get_tensor(output_details[1]['index'])

print()
import string
# Обработка результатов и вывод текста в консоль

for i in range(output_data.shape[1]):
    (x, y, w, h) = geometry[0, i, 1:5].astype(np.int32)
    text = ''
    for j in range(4, geometry.shape[2]):
        # print(geometry[0, i, j])
        if np.any(geometry[0, i, j] != 0):
            char = chr(int(geometry[0, i, j][0]))
            if char.isprintable() and char in string.printable:
                text += chr(int(geometry[0, i, j][0])).encode('utf-8').decode('utf-8')
    print('Текст:', text)



# # _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
#
# equalized_image = cv2.equalizeHist(gray_image)
# normalized_image = cv2.normalize(gray_image, None, 0, 255, cv2.NORM_MINMAX)
#
#
#
# # cv2.imwrite(r'C:\Service_finance\img_receipts\new1_img.jpg', gray_image)
# cv2.imshow('Изображение', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# text_1 = pytesseract.image_to_string(image, lang='rus')
#
#
# print(text_1)




# import cv2
# import numpy as np
# import tensorflow as tf
# import pytesseract
#
#
# interpreter = tf.lite.Interpreter(model_path=path_)
# interpreter.allocate_tensors()
# input_details = interpreter.get_input_details()
# output_details = interpreter.get_output_details()
#
#
# image = cv2.imread(r'C:\Service_finance\img_receipts\photo_2023-10-25_20-11-16.jpg')
#
# image = cv2.resize(image, (320, 320))
# image = np.reshape(image, (1, 320, 320, 3))
#
# image = image.astype(np.float32)
# image = image / 255.0
#
# blob = cv2.dnn.blobFromImage(image, 1.0, (320, 320), (123.68, 116.78, 103.94), True, False)
#
# interpreter.set_tensor(input_details[0]['index'], blob)
# interpreter.invoke()
#
#
# output_data = interpreter.get_tensor(output_details[0]['index'])
# scores = output_data[0, 0, :, 2]
# geometry = output_data[0, 0, :, 3:7]
# indices = np.where(scores > 0.5)
#
#
# for i in indices[0]:
#     angle = geometry[i, 1]
#     x, y, w, h = geometry[i, 3] * 4, geometry[i, 4] * 4, geometry[i, 5] * 4, geometry[i, 6] * 4
#     roi = image[int(y):int(y + h), int(x):int(x + w)]
#     gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#     _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#     text = pytesseract.image_to_string(threshold, lang='rus')
#     print("Распознанный текст:", text)



import cv2


def captch_ex(file_name):
    img = cv2.imread(file_name)

    img_final = cv2.imread(file_name)
    img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
    ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV
    '''
            line  8 to 12  : Remove noisy portion 
    '''
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,
                                                         3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
    dilated = cv2.dilate(new_img, kernel, iterations=9)  # dilate , more the iteration more the dilation


    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # findContours returns 3 variables for getting contours

    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)

        # Don't plot small false positives that aren't text
        if w < 35 and h < 35:
            continue

        # draw rectangle around contour on original image
        cv2.rectangle(image_final, (x, y), (x + w, y + h), (255, 0, 255), 2)

        '''
        #you can crop image and send to OCR  , false detected will return no text :)
        cropped = img_final[y :y +  h , x : x + w]

        s = file_name + '/crop_' + str(index) + '.jpg' 
        cv2.imwrite(s , cropped)
        index = index + 1

        '''
    # write original image with added contours to disk
    cv2.imshow('captcha_result', image_final)
    cv2.waitKey()


# file_name = r'C:\Service_finance\img_receipts\photo_2023-10-25_20-11-16.jpg'
# captch_ex(file_name)



import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image, convert to HSV format, define lower/upper ranges, and perform
# color segmentation to create a binary mask
image = cv2.imread(r'/cost_calculations/img_receipts\photo_2023-10-25_20-11-16.jpg')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 0])
upper = np.array([179, 255, 30])
mask = cv2.inRange(hsv, lower, upper)

# Create horizontal kernel and dilate to connect text characters
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,3))
dilate = cv2.dilate(mask, kernel, iterations=5)

# Find contours and filter using aspect ratio
# Remove non-text contours by filling in the contour
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    ar = w / float(h)
    if ar < 5:
        cv2.drawContours(dilate, [c], -1, (0,0,0), -1)

# Bitwise dilated image with mask, invert, then OCR
result = 255 - cv2.bitwise_and(dilate, mask)
# data = pytesseract.image_to_string(result, lang='rus', config='--psm 6')
# print(data)

# cv2.imshow('mask', mask)
# cv2.imshow('dilate', dilate)
# cv2.imshow('result', result)
# cv2.waitKey()



import cv2
import numpy as np

# Загрузка изображения
image = cv2.imread(r'/cost_calculations/img_receipts\photo_2023-10-25_20-11-16.jpg')

# Преобразование изображения в оттенки серого

binary_image = cv2.bitwise_not(image)
gray_1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.cvtColor(binary_image, cv2.COLOR_BGR2GRAY)

# Применение порогового значения для получения двоичной маски
_, binary_mask = cv2.threshold(gray_1, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# binary_image = cv2.bitwise_not(gray)

lower = np.array([95], dtype=np.uint8)
upper = np.array([255], dtype=np.uint8)

# lower = np.array([0, 0, 218], dtype=np.uint8)
# upper = np.array([157, 54, 255], dtype=np.uint8)
mask = cv2.inRange(gray, lower, upper)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 3))
dilate = cv2.dilate(mask, kernel, iterations=5)


# dilate_origin = cv2.dilate(binary_mask, kernel, iterations=5)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    ar = w / float(h)
    if ar < 5:
        cv2.drawContours(dilate, [c], -1, (0, 0, 0), 1)

# Bitwise dilated image with mask, invert, then OCR
result = 255 - cv2.bitwise_and(dilate, mask)
data = pytesseract.image_to_string(result, lang='rus', config='--psm 6')
print(data)

# Отображение двоичной маски
cv2.imshow('Binary Mask', gray)
cv2.imshow('dilate', dilate)
cv2.imshow('result', result)
# cv2.imshow('dilate_origin', dilate_origin)
# cv2.imshow('result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()