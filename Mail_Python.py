import smtplib   # Импортируем библиотеку по работе с SMTP
from email.mime.multipart import MIMEMultipart  #позволяет создавать объекты из нескольких составляющих
from email.mime.text import MIMEText  # тип MIMEText позводяет отправлять кириллицу
from email.mime.application import MIMEApplication  # позволяет преобразовывать файлы для отправки
from os.path import basename   # функция basename(name_file) позволяет передать имя файла и его расширение

def main_send_mail(theme_letter, text_letter):
    from_email = 'zerg_exidna@mail.ru'
    recipients = ['chernyshov.sp@erkapharm.com']
                  #chernyshov.sp@erkapharm.com, exidna3@bk.ru, 'mironov.ai@erkapharm.com',
    #msg_simple = MIMEText('Проверка') #Тип MIMEText позвлояет отправлять сообщения в кириллице
    my_messenge = MIMEMultipart()  # Создаем переменную MIMEMultipart, в которую можно складывать
                            # всю информацию о нашем письме (адреса, тема, текст, картинки, html и т.д.

    my_messenge['Subject'] = theme_letter    # Добавляем тему письма
    my_messenge['From'] = 'Python-script <' + from_email + '>'  # Этот текст отобразится в заголовке письма
    my_messenge['To'] = ', '.join(recipients)       # формируем список адресов получателей
    #my_messenge['Reply-To'] = from_email        # указываем на какой адрес надо отвечать

    #text = 'Мое сообщение: Требуется заменить ФН в ККМ №_______, установленной по адресу_____' # Текстовый вариант письма
    part_text = MIMEText(text_letter, 'plain')
    my_messenge.attach(part_text)

    name_file = 'logo.png'    # Указываем имя файла, который будет во вложении (должен лежать в этой папке с проектом)
    with open(name_file, 'rb') as file: file_mail = MIMEApplication(file.read(), Name=basename(name_file))
    #file_mail = MIMEApplication(open(name_file, 'rb').read(), Name=basename(name_file))   # АНАЛОГ предыдущей строки
                #через функцию MIMEApplication формируем вложение из файла,
                #'rb' - Открывает файл в бинарном режиме только для чтения. Это режим "по умолчанию".
                #часть "Name=basename(name_file)" передает имя файла и его расширение, иначе файл придет как "Untitled.bin"
    my_messenge.attach(file_mail)   # Вкладывыаем вложениe в сообщение

    server = smtplib.SMTP('smtp.mail.ru', 25)    # Создаем объект SMTP
    server.starttls()                                  # Начинаем шифрованный обмен по TLS
    server.login('zerg_exidna@mail.ru', 'pbCHKE5Hv59gmhLEFHQt')    # Получаем доступ к почте отправителя
    server.sendmail(from_email, recipients, my_messenge.as_string())
    server.quit()                                       # Выходим

if __name__ == '__main__':
    main_send_mail('Тема письма', 'Текст письма')

''' ЧУЖОЙ   КОД   ДЛЯ   ОБУЧЕНИЯ:
import smtplib                                              # Импортируем библиотеку по работе с SMTP
import os                                                   # Функции для работы с операционной системой, не зависящие от используемой операционной системы

# Добавляем необходимые подклассы - MIME-типы
import mimetypes                                            # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders                                  # Импортируем энкодер
from email.mime.base import MIMEBase                        # Общий тип
from email.mime.text import MIMEText                        # Текст/HTML
from email.mime.image import MIMEImage                      # Изображения
from email.mime.audio import MIMEAudio                      # Аудио
from email.mime.multipart import MIMEMultipart              # Многокомпонентный объект


def send_email(addr_to, msg_subj, msg_text, files):
    addr_from = "my_addr@server.ru"                         # Отправитель
    password  = "password"                                  # Пароль

    msg = MIMEMultipart()                                   # Создаем сообщение
    msg['From']    = addr_from                              # Адресат
    msg['To']      = addr_to                                # Получатель
    msg['Subject'] = msg_subj                               # Тема сообщения

    body = msg_text                                         # Текст сообщения
    msg.attach(MIMEText(body, 'plain'))                     # Добавляем в сообщение текст

    process_attachement(msg, files)

    #======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================================
    server = smtplib.SMTP_SSL('smtp.server.ru', 465)        # Создаем объект SMTP
    #server.starttls()                                      # Начинаем шифрованный обмен по TLS
    #server.set_debuglevel(True)                            # Включаем режим отладки, если не нужен - можно закомментировать
    server.login(addr_from, password)                       # Получаем доступ
    server.send_message(msg)                                # Отправляем сообщение
    server.quit()                                           # Выходим
    #==========================================================================================================================

def process_attachement(msg, files):                        # Функция по обработке списка, добавляемых к сообщению файлов
    for f in files:
        if os.path.isfile(f):                               # Если файл существует
            attach_file(msg,f)                              # Добавляем файл к сообщению
        elif os.path.exists(f):                             # Если путь не файл и существует, значит - папка
            dir = os.listdir(f)                             # Получаем список файлов в папке
            for file in dir:                                # Перебираем все файлы и...
                attach_file(msg,f+"/"+file)                 # ...добавляем каждый файл к сообщению

def attach_file(msg, filepath):                             # Функция по добавлению конкретного файла к сообщению
    filename = os.path.basename(filepath)                   # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)        # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:               # Если тип файла не определяется
        ctype = 'application/octet-stream'                  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)                 # Получаем тип и подтип
    if maintype == 'text':                                  # Если текстовый файл
        with open(filepath) as fp:                          # Открываем файл для чтения
            file = MIMEText(fp.read(), _subtype=subtype)    # Используем тип MIMEText
            fp.close()                                      # После использования файл обязательно нужно закрыть
    elif maintype == 'image':                               # Если изображение
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'audio':                               # Если аудио
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
    else:                                                   # Неизвестный тип файла
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
            file.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()
            encoders.encode_base64(file)                    # Содержимое должно кодироваться как Base64
    file.add_header('Content-Disposition', 'attachment', filename=filename) # Добавляем заголовки
    msg.attach(file)                                        # Присоединяем файл к сообщению



# Использование функции send_email()
addr_to   = "xxxx@server.ru"                                # Получатель
files = ["file1_path",                                      # Список файлов, если вложений нет, то files=[]
         "file2_path",                                      
         "dir1_path"]                                       # Если нужно отправить все файлы из заданной папки, нужно указать её

send_email(addr_to, "Тема сообщения", "Текст сообщения", files)
'''