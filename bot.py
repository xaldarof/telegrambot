import requests
import telebot
import json

token = "5160537118:AAFuMZilFGID06jgrNp5pvIP6g8Mny3NUHg"
api_key = "ecdda7f610b72f3e111a6ee021d7f234"
bot = telebot.TeleBot(token)



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Salom")


@bot.message_handler(content_types=["text"])
def echo(message):
    response = request_to_api(message.text)

    if response.status_code == 200:
        formatted = json.loads(response.text)
    else:
        bot.send_message(message.chat.id, "Данный город не найден 😪")


def request_to_api(city):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
    return response


bot.infinity_polling()
