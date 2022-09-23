#my_first_bot_zzz

from NalogKKM import *


import telebot
bot = telebot.TeleBot("1519526915:AAGnz5H4khS2bD44CZKePX2pN4avbyOpkko", parse_mode=None)

# Эта конструкция (строчки, помеченные bot.message) из библиотеки pyTelegramBotAPI,
# которая перехватывает все сообщения:
@bot.message_handler(func=lambda m: True)     #bot.message
def echo_all(message):                        #bot.message
    df = pd.read_excel('data_frame.xlsx', dtype={'RNN': str, 'ZN_KKM': str})
    delta_day = message.text
    if delta_day.isdigit():   # проверяем, состоит ли полученное из телеги цифрами
        delta_day = int(message.text)   # переводим цифры в число
        df_control = selection_df(df, delta_day) # Функция для выбора ККМ,
                                                 # у которых истекает срок действия ФН (от сегодня до+delta_day дней)
        list = listed_statement(df_control)     # Функция преобразует датафрейм в список
        if len(list) == 0:
            print('В данный промежуток времени замена ФН не требуется.')
            return
        else:
            volume_print = f'В ближайшие {delta_day} дней требуется провести замену {len(list)} фискальных накопителей: \n'
            for l_temp in list:     # итерируем список по элементам (каждый элемент - инфа об одной ККМ для замены ФН)
                volume_print += l_temp[2] + '\n'
            print(volume_print)
    else: volume_print = 'Вы ввели неправильное число'
    bot.reply_to(message, volume_print)       #bot.message    -- отпралвляет сообщение


bot.polling()                   # Эта команда запускает самого бота
