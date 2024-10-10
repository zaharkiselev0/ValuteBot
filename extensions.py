import requests
import json
import time

import config


class StaticMessages:
    def __init__(self):
        self.message_texts = dict()
        help_text = ("Я помогу получить данные об актуальном курсе валют ЦБ РФ.\n"
                     "Введите одну из команд:\n"
                     "[Код валюты] [Код валюты] [Количество] - "
                     "узнать цену первой валюты в заданном количестве во второй валюте\n"
                     "Пример: EUR USD 100 - возвращает цену 100 евро в долларах.\n"
                     "/values - возвращает все доступные коды и названия валют.\n"
                     "/time - время последнего обновления данных.\n"
                     "/help - вывести это сообщение")
        self.message_texts['/start'] = help_text
        self.message_texts['/help'] = help_text

    def update(self, data):
        valutes = data['Valute']

        values_lines = ["Данные о валютах в формате [код валюты] - [название валюты]:"]
        values_lines.extend([f"{valutes[valute]['CharCode']} - {valutes[valute]['Name']}" for valute in
                             sorted(valutes.keys())])
        value_text = '\n'.join(values_lines)
        self.message_texts['/values'] = value_text

        self.message_texts['/time'] = data['Timestamp'][:10] + ' ' + data['Timestamp'][11:16]


class Valutes:
    def __init__(self, static_messages: StaticMessages):
        self.valutes = dict()
        self.static_messages = static_messages
        self.update()

    def run(self):
        while True:
            self.update()
            time.sleep(config.update_time)

    def update(self):
        json_data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        data = json.loads(json_data.content)
        data['Valute']['RUB'] = {'CharCode': 'RUB', 'Nominal': 1, 'Name': 'Российский рубль', 'Value': 1}
        self.valutes = data['Valute']
        self.static_messages.update(data)


static_messages = StaticMessages()
valutes = Valutes(static_messages)
