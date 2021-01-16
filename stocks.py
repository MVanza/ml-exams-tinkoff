import csv


FILE_NAME = 'new.csv'


# функция для получение среднего и средне скользящего значения из файла
def get_av(moving_average_value):
    """
    Для разных ситуаций подбираем разный коэфициент для скользящей средней
    """
    if moving_average_value == 1:
        moving_average_value = 15
    elif moving_average_value == 2:
        moving_average_value = 11
    else:
        moving_average_value = 10
    with open(FILE_NAME, newline='') as csvfile:
        data = csv.reader(csvfile)
        start = True
        dtp = []
        for i in data:
            if start:
                start = False
                continue
            dtp.append([int(i[1]), int(i[2]), float(i[3])])
    mav = []
    s = 0
    for i in range(len(dtp)):
        if i % moving_average_value == 0:
            s = float(dtp[i][2])
            mav.append(s)
        else:
            mav.append((dtp[i][2] + s) / 2)
    return dtp, mav


"""
Основа торгов построенна на следующем принципе:
Если скользящая средняя пересекает среднюю снизу - покупаем.
Если скользящая средняя пересекает среднюю сверху - продаём.
"""


def analyse1():   # 1 случай
    dtp, mav = get_av(1)
    date, time = [x[0] for x in dtp], [x[1] for x in dtp]
    mup = False
    dollar_value = 0
    stocks = 0
    for i in range(len(dtp)):
        if dtp[i][2] < mav[i]:
            if not mup:
                dollar_value -= dtp[i][2]
                stocks += 1
                mup = True
                print(f'Произведена покупка 1 акции {date[i]} в {time[i]} по цене {dtp[i][2]}')
            else:
                continue

        elif dtp[i][2] > mav[i]:
            if mup and stocks > 0:
                dollar_value += dtp[i][2]
                print(f'Произведена продажа 1 акции {date[i]} в {time[i]} по цене {dtp[i][2]}.\n'
                      f'Заработанная сумма - {dollar_value}')
                break
            else:
                continue


def analyse2():  # 2 случай
    dtp, mav = get_av(2)
    date, time = [x[0] for x in dtp], [x[1] for x in dtp]
    mup = False
    dollar_value = 0
    stocks = 0
    j = 0
    for i in range(len(dtp)):
        if dtp[i][2] < mav[i]:
            if not mup:
                dollar_value -= dtp[i][2]
                stocks += 1
                print(f'Произведена покупка 1 акции {date[i]} в {time[i]} по цене {dtp[i][2]}')
                mup = True
            else:
                continue

        elif dtp[i][2] > mav[i]:
            if mup and stocks > 0:
                dollar_value += dtp[i][2]
                print(f'Произведена продажа 1 акции {date[i]} в {time[i]} по цене {dtp[i][2]}.')
                j += 1
                stocks = 0
                mup = False
                if j == 2:
                    print(f'Заработанная сумма - {dollar_value}')
                    break
            else:
                continue


def analyse3(K, dollar_value):  # 3 случай
    dtp, mav = get_av(3)
    date, time = [x[0] for x in dtp], [x[1] for x in dtp]
    mup = False
    stocks = 0
    dv = dollar_value
    j = 0
    for i in range(len(dtp)):
        if dtp[i][2] < mav[i]:
            if not mup:
                if dv > dtp[i][2]:
                    dv -= dtp[i][2]
                    stocks += 1
                    print(f'Произведена покупка 1 акции {date[i]} в {time[i]} по цене {dtp[i][2]}')
                else:
                    print(f'Ушёл в минус: {dv - dollar_value}')
                mup = True
            else:
                continue

        elif dtp[i][2] > mav[i]:
            if mup and stocks > 0:
                dv += dtp[i][2]
                print(f'Произведена продажа 1 акции {date[i]} в {time[i]} по цене {dtp[i][2]}.')
                j += 1
                stocks = 0
                mup = False
                if j == K:
                    print(f'Заработанная сумма - {dv - dollar_value}')
                    break
            else:
                continue


analyse1()  # заработок 5
analyse2()  # заработок 5
analyse3(100, 2000)  # заработок 266
