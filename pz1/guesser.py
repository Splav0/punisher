import random

def main():
    """Угадайка"""
    number = random.randint(0, 100)
    while True:
        answer = input('Угадайте число: ')
        # если ввести не число, то всё поломается. Обработку ошибок рассмотрим позже

        if True == answer.isdigit():
            answer = int(answer)

            if answer == number:
                print('Успех')
                break

            elif answer < number:
                print('Бери выше')
            else:
                print('Бери ниже')

        elif answer == 'exit':
            print(f"Выход, было загадано число: {number}.")
            break
        else:
            print('Введено не числовое значение')

if __name__ == '__main__':
    main()



