#my_first_bot_zzz
from NalogKKM import *


import telebot
bot = telebot.TeleBot("1519526915:AAGnz5H4khS2bD44CZKePX2pN4avbyOpkko", parse_mode=None)

from pyowm import OWM
owm = OWM('8a0792fd900a9fc2244f2db313b1f960')

# Эта конструкция (строчки, помеченные bot.message) из библиотеки pyTelegramBotAPI,
# которая перехватывает все сообщения:
@bot.message_handler(func=lambda m: True)     #bot.message
def echo_all(message):                        #bot.message
    list = main_kkm()
    for i in list: print(i[2])


    bot.reply_to(message, volume_print)  # bot.message

bot.polling()  # Эта команда запускает самого бота
