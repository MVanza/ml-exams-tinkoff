import random
import pickle


def transpose(field):
    return list(map(list, zip(*field)))


def swap_rows_small(field):
    """
    Обмен двух строк в пределах одного района
    """
    # получение случайного района и случайной строки
    area = random.randrange(0, 3, 1)
    line1 = random.randrange(0, 3, 1)
    # номер 1 строки для обмена
    N1 = area * 3 + line1

    line2 = random.randrange(0, 3, 1)
    while line1 == line2:
        line2 = random.randrange(0, 3, 1)
    # номер 2 строки для обмена
    N2 = area * 3 + line2
    field[N1], field[N2] = field[N2], field[N1]
    return field


def swap_columns_small(field):
    field = transpose(field)
    field = swap_rows_small(field)
    return transpose(field)


def swap_rows_area(field):
    """
    Обмен двух районов по горизонтали
    """
    area1 = random.randrange(0, 3, 1)
    # получение случайного района

    area2 = random.randrange(0, 3, 1)
    while area1 == area2:
        area2 = random.randrange(0, 3, 1)

    for i in range(0, 3):
        N1, N2 = area1 * 3 + i, area2 * 3 + i
        field[N1], field[N2] = field[N2], field[N1]
    return field


def swap_columns_area(field):
    field = transpose(field)
    field = swap_rows_area(field)
    return transpose(field)


class Sudoku:
    def __init__(self, mode, field_size):
        self.mode = mode
        self.field = self.make_field(field_size)

    def make_field(self, field_size):
        base_field = [[((i*3 + i/3 + j) % (3*3) + 1) for j in range(3*3)] for i in range(3*3)]
        shuffle_func = ['transpose(base_field)', 'swap_rows_small(base_field)',
                        'swap_columns_small(base_field)', 'swap_rows_area(base_field)',
                        'swap_columns_area(base_field)']
        for _ in range(10):
            base_field = eval(shuffle_func[random.randrange(0, len(shuffle_func), 1)])
        return base_field


class AISudoku(Sudoku):
    """
    Класс для игры с компьютером
    """
    pass


class PlayerSudoku(Sudoku):
    """
    Класс для игры с человеком
    """
    def save_field(self):
        pass

    def download_field(self):
        pass


def run_func():
    print('Welcome to sudoku. Who will play: you or computer?')
    inp = input()
    if inp == 'me':
        print('Cool! Now enter the field size')
        fs = int(input())
        player = PlayerSudoku('p', fs)
        return player
    elif inp == 'computer':
        print('Great! Now enter the field size')
        fs = int(input())
        comp = AISudoku('c', fs)
        return comp
    else:
        print('No, it\'s just 2 variant. Try again')
        return run_func()


if __name__ == '__main__':
    c = run_func()

