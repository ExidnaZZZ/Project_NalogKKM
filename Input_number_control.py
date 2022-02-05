def main_input_number(quantity_figure=2):
    temp = True
    while temp:
        number = input(f'Введите число от 1 до {str(9)*quantity_figure}\n')
        temp = False
        if (len(number)-1 < quantity_figure):
            for i in range(len(number)):
                if number[i] not in '0123456789':
                    print(f'Вы ввели ввели символ \"{number[i]}", который не является цифрой, его следует заменить!')
                    temp = True
        else:
            print(f'Вы ввели неправильное число, содержащее сильно много символов \n'
                  f'(необходимо вводить число от 1 до {str(9)*quantity_figure}). \n\n'
                  'Повторите попытку')
            temp = True
    number = int(number)
    return(number)
    #print(f'Ура! Вы ввели правильное число, равное {number}')

if __name__ == '__main__':
    main_input_number(quantity_figure=2)