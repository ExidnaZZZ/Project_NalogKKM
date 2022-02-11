#my_first_bot_zzz

from NalogKKM import *
import pandas as pd


import telebot
bot = telebot.TeleBot("1519526915:AAGnz5H4khS2bD44CZKePX2pN4avbyOpkko", parse_mode=None)

# Эта конструкция (строчки, помеченные bot.message) из библиотеки pyTelegramBotAPI,
# которая перехватывает все сообщения:
@bot.message_handler(func=lambda m: True)     #bot.message
def echo_all(message):                        #bot.message
    print('delta_day')
    df = pd.read_excel('data_frame.xlsx', dtype={'RNN': str, 'ZN_KKM': str})
    delta_day = message.text
    print(delta_day)
    if delta_day.isdigit():
        delta_day = int(message.text)
        df_control = selection_df(df, delta_day) # Функция для выявления ККМ, у которых истекает срок действия ФН (запас 20 дней)
        list = listed_statement(df_control)
        if len(list) == 0:
            print('В данный промежуток времени замена ФН не требуется.')
            return
        else:
            volume_print = f'В ближайшие {delta_day} дней требуется провести замену {len(list)} фискальных накопителей: \n'
            for l_temp in list:
                volume_print += l_temp[2] + '\n'
            print(volume_print)
    else: volume_print = 'Вы ввели неправильное число'
    bot.reply_to(message, volume_print)       #bot.message


bot.polling()                   # Эта команда запускает самого бота
