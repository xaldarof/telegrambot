import datetime
import json

import requests
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime as time

token = "5160537118:AAHr2RUc4bUkfy9mAzFVl_Fa-i3JGfQp_Ek"
api_key = "ecdda7f610b72f3e111a6ee021d7f234"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Привет {message.chat.first_name} этот бот был создан Темуром\n\n"
                                      "Отправьте мне имя места и получи информацию о погоде...😊")


@bot.message_handler(content_types=["text"])
def echo(message):
    if message.text.startWith("/"):
        response = request_to_api(message.text)
        dict = {"Открыть на карте": "John"}
        buttons = []

        if response.status_code == 200:
            formatted = json.loads(response.text)
            dateTimeSunset = time.datetime.fromtimestamp(
                (formatted['sys']['sunrise'])).strftime('%H:%M:%S')
            dateTimeSunrise = time.datetime.fromtimestamp(
                (formatted['sys']['sunset'])).strftime('%H:%M:%S')

            done = f"Информация о городе : \n🔎 {message.text}\n" \
                   f"\n😊 Температура  : {formatted['main']['temp']}" \
                   f"\n❤ Ощущается : {formatted['main']['feels_like']}" \
                   f"\n🤷‍ Мин. температура :  {formatted['main']['temp_min']}" \
                   f"\n😃 Макс. температура :  {formatted['main']['temp_max']}" \
                   f"\n🌪 Скорость ветра : {formatted['wind']['speed']} " \
                   f"\n🌞 Восход солнца :  {dateTimeSunset}" \
                   f"\n🌘 Закат : {dateTimeSunrise}"

            for key, value in dict.items():
                buttons.append([InlineKeyboardButton(text=key,
                                                     url=f"https://maps.google.com/?q={formatted['coord']['lat']},{formatted['coord']['lon']}&lang=ru")])

                keyboard = InlineKeyboardMarkup(buttons)
                bot.send_message(message.chat.id, reply_markup=keyboard, text=done)

        else:
            bot.send_message(message.chat.id, "Данный город не найден 😪")
    else:
        bot.reply_to(message,"😊 Для поиска вы должны начать слово с /")

def request_to_api(city):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
    return response


bot.infinity_polling()
