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


def get_random_square(field, square_num):
    j = 0
    for i in range(81 - square_num):
        row = random.randrange(0, 9, 1)
        columns = random.randrange(0, 9, 1)
        if field[row][columns] != '_':
            field[row][columns] = '_'
            j += 1
        else:
            field = get_random_square(field, square_num + j)
    return field


class Sudoku:

    @staticmethod
    def make_field(field_size):
        base_field = [[int(((i*3 + i/3 + j) % (3*3) + 1)) for j in range(3*3)] for i in range(3*3)]
        shuffle_func = ['transpose(base_field)', 'swap_rows_small(base_field)',
                        'swap_columns_small(base_field)', 'swap_rows_area(base_field)',
                        'swap_columns_area(base_field)']
        # перемещаем нашу таблицу 10 раз
        for _ in range(10):
            base_field = eval(shuffle_func[random.randrange(0, len(shuffle_func), 1)])

        # удаляем случайные клетки
        new_field = get_random_square(base_field, field_size)
        return new_field


class AISudoku(Sudoku):
    """
    Класс для игры с компьютером
    """

    pass


class PlayerSudoku(Sudoku):
    """
    Класс для игры с человеком
    """
    ans = []

    def __init__(self, field_size):
        self.field_size = field_size
        self.field = []
        self.download_field()

    def save(self):
        with open('data.pkl', 'wb') as file:
            pickle.dump(self.field, file)

    def __del__(self):
        self.save()

    def download_field(self):
        try:
            f = open('data.pkl', 'rb')
            if pickle.load(f) != '':
                self.field = pickle.load(f)
            else:
                self.field = self.make_field(self.field_size)
            f.close()
        except FileNotFoundError:
            self.field = self.make_field(self.field_size)
            self.ans = self.field
        except EOFError:
            self.field = self.make_field(self.field_size)
            self.ans = self.field

    def play(self):
        for i in range(9):
            print(self.field[i])
        print('Enter square coordinate and square value')
        inp = input().split()
        if inp[0] == 'q':
            del self.field
            return 'q'
        if self.field[int(inp[0]) - 1][int(inp[1]) - 1] != '_':
            print('No, you can\'t do it like this. Try again')
            return 0
        else:
            print('Ok')
            self.field[int(inp[0]) - 1][int(inp[1]) - 1] = int(inp[2])
            return 1

    def check_ans(self):
        if self.ans == self.field:
            return 'Well done, my freind!'
        else:
            return 'Try better next time!'


def run_func():
    print('Welcome to sudoku. Who will play: you or computer?')
    inp = input()
    if inp == 'me':
        print('Cool! Now enter the field size')
        fs = int(input())
        player = PlayerSudoku(fs)
        return player
    elif inp == 'computer':
        print('Great! Now enter the field size')
        fs = int(input())
        return AISudoku()
    else:
        print('No, it\'s just 2 variant. Try again')
        return run_func()


if __name__ == '__main__':
    while True:
        c = run_func()
        k = 0
        ans = ''
        while True:
            t = c.play()
            if t == 'q':
                c.save()
                break
            else:
                k += t
                if k == (81 - c.field_size):
                    print(c.check_ans())
                    print('Wanna play again? yes or no')
                    ans = input()
                    f = open('data.pkl', 'wb')
                    pickle.dump('', f)
                    f.close()
                    break
        if ans == 'yes':
            continue
        elif ans == 'no':
            break

