import telebot
import threading

import config
from extensions import valutes, static_messages


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['values', 'start', 'help', 'time'])
def static_message(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, static_messages.message_texts[message.text])


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message) -> None:
    try:
        base, quote, amount = message.text.split()
    except ValueError as e:
        bot.send_message(message.chat.id, "Неверное количество переменных")
        return

    try:
        amount = float(amount)
        values = valutes.valutes
        price = amount * values[base]['Value'] / values[base]['Nominal'] * values[quote]['Nominal'] / values[quote]['Value']
        bot.send_message(message.chat.id, f"{amount} {values[base]['Name']} стоит {price} {values[quote]['Name']}")
    except ValueError as e:
        bot.send_message(message.chat.id, "Количество валюты должно быть числом")
    except KeyError as e:
        bot.send_message(message.chat.id, f"Неизвестный код валюты: '{e}'\n"
                                          "Для получения информации о кодах валют введите /values")


th1 = threading.Thread(target=valutes.run, args=([]), daemon=True)
th2 = threading.Thread(target=lambda: bot.polling(), args=([]), daemon=True)
th1.start()
th2.start()
th1.join()
th1.join()
