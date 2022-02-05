import pandas as pd
import os
import datetime
from Input_number_control import *

def address(kkm_control):      #  функция преобразует Addres_KKM из переданных данных типа Series в удобочитаемый вид
    list_address = list(kkm_control['Addres_KKM'])   # из Addres_KKM типа string создаем посимвольный список типа [Н,о,в,о,с,и,б,...]
    list_address = ''.join(list_address).split(',')  # Приводим список к виду [630049, Новосибирск, ....]
    list_temp = []                                      # Создаем пустой временный список
    for i in [0,5,6,8,9,10]:                            # в данном цикле выбираем из списка нужные данные
        if list_address[i] != ' ' and list_address[i] != '':  # здесь убираем пустоты и лишние пробелы
            if (list_address[i][-4:] == 'сети'): list_address[i] = list_address[i][0:-28] # здесь убираем лишние символы
            list_temp.append(list_address[i])        # складывем нужные данные
    return (','.join(list_temp))         # возвращаем полученный адрес в виде списка

def splin_zn (l):
    l = list(l)
    for i in [12,8,4,0]: l.insert(i,' ')
    return(''.join(l))


def connect_df():      # Функция для сбора всех файлов-выгрузок из налоговой
    name_file_all = pd.DataFrame()
    #name_file_all = pd.read_csv('Nalog_KKM/Sibirs2.csv', sep=';')
    for file in os.listdir('Nalog_KKM/'):
            tmp = pd.read_csv('Nalog_KKM/' + file, sep=';',
                              dtype={'Регистрационный номер': str,
                                     'Заводской номер ККТ': str,
                                     'Заводской номер ФН': str}) #Создаем DF так, чтобы не обрезать нули в номерах
            tmp.insert(0, 'Region', file[:-4])  # Вставляем столбец с наименованием юрлица
            name_file_all = pd.concat([name_file_all, tmp])
    name_file_all.reset_index(inplace=True, drop=True)
    return (name_file_all)



def prepare_df(df):     # Функция для подготовки датафрейма:
                        #убираем лишние столбцы, переименовываем нужные, уточняем формат данных
    df = df.rename(columns={                       # Переименовываем столбцы в более удобный вид
        'Срок окончания действия ФН': 'End_FN',
        'Дата регистрации ККТ в НО': 'Date_KKM',
        'Адрес места установки': 'Addres_KKM',
        'Регистрационный номер':'RNN',
        'Модель': 'Name_KKM',
        'Состояние': 'Property_KKM',
        'Заводской номер ККТ': 'ZN_KKM',
        'Наименование ОФД': 'OFD',
        'Заводской номер ФН': 'ZN_FN'
    })
    df = df.iloc[:,:10]     #срезать лишние столбцы
    df = df[~df['End_FN'].isnull()] # удаление строки, где в слобце 'Срок окончания действия ФН' нет значений,
                        # т.е. стоит Nan
    df['End_FN'] = pd.to_datetime(df.End_FN, format='%d.%m.%Y %H:%M:%S')   #данные столбца End_FN в ДатаВремя
    df['Date_KKM'] = pd.to_datetime(df.Date_KKM, format='%d.%m.%Y %H:%M:%S')  #данные столбца Date_KKM в ДатаВремя
    df.reset_index(drop=True, inplace=True)    # После соединения DF и удаления строк сбиваются индексы,
                                                # данная команда проставляет их заново
    return (df)

def selection_df(df, delta_day):    # Функция для выявления ККМ, у которых истекает срок действия ФН (запас 20 дней)
    date1 = datetime.datetime.today()   # Определяем дату на данный момент
    date2 = date1 + datetime.timedelta(days=delta_day) # Определяем контрольную (крайнюю) дату
    df_control = df[(df.End_FN > date1) & (df.End_FN < date2)]  # Создаем контрольный датафрейм с выборкой по времени
    df_control.reset_index(inplace=True, drop=True)             # переопрделяем в нем индексы
    return (df_control)

def listed_statement(df_control):   #Функция распечатки заявок на замену ФН
    list_statement = []
    for i in range(len(df_control)):  # Цикл для перебора контольного фрейма
        addres_KKM = address(df_control.iloc[i,:])   # Используем функцию address для получения адреса в читаемом виде
        #rnn_kkm = df_control.loc[i,'RNN']
        zn_kkm = splin_zn(df_control.loc[i, 'ZN_KKM'])  # Используем функцию splin_zn для резделения номера на октеты
        srok_fn= df_control.loc[i, 'End_FN'].strftime('%d-%m-%Y')  # Дату-время преобразуем в текстовую дату
        name_kkm = df_control.loc[i, 'Name_KKM']
        list_statement.append([name_kkm, zn_kkm, addres_KKM, srok_fn])
#        list_statement.append(f'''Произвести замену ФН на ККМ типа {name_kkm}) \
#с заводским номером №{zn_kkm} на торговой точке по адресу: {addres_KKM}. \
#Крайний срок замены ФН - {srok_fn}.''')
    return(list_statement)


def main_kkm():
    if os.path.isfile('data_frame.xlsx'):
        date_modificated_file_xlsx = os.path.getmtime('data_frame.xlsx')  # дата последнего изменения файла 'data_frame.xlsx' в формате типа <class 'float'>
    else:
        print('Сохраненного ранее файла "data_frame.xlsx" с результатами анализа выгрузки из налоговой не существует. \n\n'
              'Производится новый анализ файлов-выгрузок из налоговой и его сохранение в "data_frame.xlsx"...')
        date_modificated_file_xlsx = float(0)
    if os.path.isfile('nalog_KKM\ЭркаСиб.csv'):
        date_upload_file_nalog = os.path.getmtime('nalog_KKM\ЭркаСиб.csv')  # дата последнего изменения файла 'data_frame.xlsx' в формате типа <class 'float'>
    else:
        print('В папке "\\nalog_KKM\" отсутствует файл "ЭркаСиб.csv", проверьте наличие файлов-выгрузок из налоговой. \n'
              'Работа программы завершена с ошибкой, проверьте файлы в папке "\\nalog_KKM\"')
        list = ()
        return (list)
    #t2 = os.path.getctime('logo.png')  # дата создания файла в формате типа <class 'float'>
    # напечатать дату в строковом формате:
    # print(time.ctime(t2))
    date_xlsx = datetime.datetime.fromtimestamp(date_modificated_file_xlsx) # преобразование даты типа "class float" в формате <class 'datetime.datetime'>
    date_nalog = datetime.datetime.fromtimestamp(date_upload_file_nalog)  # преобразование даты типа "class float" в формате <class 'datetime.datetime'>
    if date_xlsx < date_nalog:
        print('Файл "data_frame.xlsx" обновляется....')
        df = connect_df().copy()  # Создаем рабочую копию DF используя функцию connect_df()
        df = prepare_df(df)  # Подготовка датафрейма с использованием функции prepare_df()
        df.to_excel('data_frame.xlsx', index=False)  # Сохраняем датафрейм в файл Excel
        print('Файл "data_frame.xlsx" обновлен')
        #print(df.info(), '\n\n')
    else:
        df = pd.read_excel('data_frame.xlsx', dtype={'RNN': str, 'ZN_KKM': str})
        #print(df.info())
        print('Файл "data_frame.xlsx" не требует обновления.')

    print('Введите кол-во дней, в пределах которых искать ККМ с истекающим сроком действия:  \n')
    delta_day = main_input_number(2)
    df_control = selection_df(df, delta_day)       # Подготовка датафрейма со списком ККМ, у которых истекает срок действия ФН
    list = listed_statement(df_control)
    return (list)

    #for i in list: print(i)

if __name__ == '__main__':
    main_kkm()
