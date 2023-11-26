import difflib

import requests
import csv
import cv2
import re


# Загрузка изображения
def download_image(path):
    image = cv2.imread(path)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path, gray_image)

    image_data = open(path, 'rb').read()

    # Отправка POST-запроса на OCR.space API
    api_key = 'K85148581388957'
    payload = {
        'apikey': api_key,
        'language': 'rus',
        'isOverlayRequired': False,  # Не требуется наложение текста на изображение
        'detectOrientation': True,  # Автоматическое определение ориентации текста
        'scale': True,  # Масштабирование изображения
        'filetype': 'jpg',  # Формат изображения
    }
    return image_data, payload


class OCR:
    def __init__(self, response):
        self.keyword_search = ['оплата', 'оплачено', 'оплачена', 'оплачено(плат.карта)', 'оплате', 'итого']
        self.max_similarity = float('-inf')
        self.max_number = float('-inf')  # Initializing the variable with the smallest possible value
        self.company_name_categories = []  # Сохраняется найденная фирма
        self.result_price = []  # Сохраняем текст после нахождения ключевого слова в нём, в котором может быть цена
        self.result = response.json()

        self._search_similarities()

    def _search_similarities(self):
        if self.result['IsErroredOnProcessing']:
            return 'Ошибка при обработке изображения'
        else:
            self.all_info = self.result['ParsedResults'][0]['ParsedText']

            with open(r'C:\Service_finance\cost_calculations\parser_spider\firmsdata\firmsdata\spiders\firms.csv', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                self.name_street_firm = [row for row in csv_reader][1:]

            print(self.all_info)

            try:  # Пытаемся найти название фирмы (Все фирмы выделены кавычками по бокам)
                search_company_name = self.all_info.split("”")[1].split("”")[0]
            except IndexError:
                try:
                    search_company_name = self.all_info.split("'")[1].split('”')
                    if len(search_company_name) < 1:
                        search_company_name = search_company_name[0].split("'")
                    else:
                        search_company_name = search_company_name[0]
                except IndexError:
                    search_company_name = self.all_info

            for name_firm, street, category in self.name_street_firm:
                if search_company_name:
                    similarity = difflib.SequenceMatcher(None, search_company_name, name_firm).ratio() * 100
                    if similarity >= 70:
                        if float(similarity) > self.max_similarity:
                            self.company_name_categories.clear()
                            self.max_similarity = float(similarity)
                            self.company_name_categories.extend([name_firm, category])

                else:
                    similarity = difflib.SequenceMatcher(None, self.all_info, name_firm).ratio() * 100

                    if similarity >= 60:
                        if float(similarity) > self.max_similarity:
                            self.company_name_categories.clear()
                            self.max_similarity = float(similarity)
                            self.company_name_categories.extend([name_firm, category])

            self.price_search_result = self._search_price()

    def _search_price(self):
        if self.result['IsErroredOnProcessing']:
            return 'Ошибка при обработке изображения'
        else:
            for find_word in self.keyword_search:  # Находим в тексте, есть ли ключевые слова: оплачено, итог и т.п
                if str(self.all_info).lower().find(find_word) != -1:
                    find_result_price = self.all_info.lower().split(find_word)[1]
                    price_list = find_result_price.replace(',', '.').replace(' ', '').split('\r\n')
                    self.result_price.extend(price_list)
                    break
            else:
                return 'На чеке, не найдено цены'

            for element in self.result_price:  # Находим в тексте максимальное число с точкой
                try:
                    if '.' in element and float(element) > 0:
                        if float(element) > self.max_number:
                            self.max_number = float(element)
                except ValueError:
                    continue
            if self.max_number == float('-inf'):
                return 'На чеке, не найдено цены'

    def _find_name_firm(self):
        if self.result['IsErroredOnProcessing']:
            return 'Ошибка при обработке изображения'
        else:
            delete_special_char = re.sub(r'[^\w\s]', '', self.all_info)
            result_list = delete_special_char.split('\r\n')

            for info in result_list:
                for name_firm, street, category in self.name_street_firm:
                    change_name_firm = ' '.join(word.capitalize() for word in info.split())
                    if change_name_firm.find(name_firm) != -1:
                        self.company_name_categories.extend([name_firm, category])
                        break
                else:
                    continue
                break

    def __call__(self):
        if not self.company_name_categories:
            self._find_name_firm()

            if not self.company_name_categories and self.price_search_result is None:
                return 'Не найдено название компании', self.max_number
            elif not self.company_name_categories and self.price_search_result is not None:
                return ['Не удалось распознать текст на чеке']

        if self.company_name_categories and self.price_search_result is not None:
            return self.company_name_categories[0], self.company_name_categories[1], self.price_search_result

        if self.company_name_categories and self.price_search_result is None:
            return self.company_name_categories[0], self.company_name_categories[1], self.max_number
