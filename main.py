"""На бесконечной координатной сетке находится муравей. Муравей может перемещаться на 1 клетку вверх (x,y+1),
вниз (x,y-1), влево (x-1,y), вправо (x+1,y), по одной клетке за шаг. Клетки, в которых сумма цифр в координате X плюс
сумма цифр в координате Y больше чем 25 недоступны муравью. Например, клетка с координатами (59, 79) недоступна,
т.к. 5+9+7+9=30, что больше 25. Сколько cклеток может посетить муравей если его начальная позиция (1000,1000),
(включая начальную клетку). Прислать ответ и решение в виде числа клеток и исходного текста программы на языке Python
решающей задачу."""

"""
Input:
1. Бесконечное координатное поле (x, y);
2. Муравей двигается только по прямой (диагоналей нет);
3. Если сумма цифр Х и У <= 25, то клетка доступна, иначе - нет;
4. Начальная позиция: (1000, 1000) -> sum = 2

Output:
1. Сколько свободных клеток, включая стартовую?

TODO:
1. Проверка стартовой позиции на доступность -> Сразу добавить, если доступна
2. Найти чанк, где его границы - стены
2.1 Возможно ли найти стены через подобие бинарного поиска?
3. Проверить отдельно каждую четверть графика, где центр графика - изначальное местоположение муравья
"""

from typing import Dict
from pprint import pprint
# import matplotlib.pyplot as plt

MAX_VALUE = 25  # Значение, больше которого клетка становится недоступной
dict_of_points = {}

X_START, Y_START = 1000, 1000  # TODO: Change to input()


def find_sum_of_digits(number: int) -> int:
    """

    :param number:
    :return sum_of_digits:
    """

    number_str = str(abs(number))
    sum_of_digits = 0
    for digit in number_str:
        sum_of_digits += int(digit)
    return sum_of_digits


def find_sum_of_two_digits(number_1: int, number_2) -> int:
    return find_sum_of_digits(number_1) + find_sum_of_digits(number_2)


def change_mid_number_to_less(number: int) -> int:
    """

    :param number:
    :return:
    """

    new_number = ''
    is_positive = True if number >= 0 else False
    number_list = list(str(abs(number)))
    count_of_digits = len(number_list)
    while count_of_digits != 0:
        min_digit = str(min(map(int, number_list)))
        new_number += min_digit
        number_list.pop(number_list.index(min_digit))
        count_of_digits -= 1
    if is_positive:
        new_number = int(new_number)
    else:
        new_number = 0 - int(new_number)
    return new_number


def binary_search(high: int, low: int) -> int:
    """

    :param high:
    :param low:
    :return:
    """
    mid = (high + low) // 2
    if (low == X_START and high == X_START + 1998) or (low == X_START - 1998 and high == X_START):
        sum_of_digits = find_sum_of_two_digits(mid, Y_START)
    else:
        sum_of_digits = find_sum_of_two_digits(mid, X_START)

    while sum_of_digits != MAX_VALUE:
        if MAX_VALUE > sum_of_digits:
            if mid >= 0:
                low = mid
            else:
                high = mid
        elif MAX_VALUE < sum_of_digits:
            if mid >= 0:
                high = mid
            else:
                low = mid

        mid = (high + low) // 2
        if (low == X_START and high == X_START + 1998) or (low == X_START - 1998 and high == X_START):
            sum_of_digits = find_sum_of_two_digits(mid, Y_START)
        else:
            sum_of_digits = find_sum_of_two_digits(mid, X_START)
    return change_mid_number_to_less(mid)


def find_border(x_start: int, y_start: int, direction: str) -> int:
    match direction:
        case '+x':
            high = x_start + 1998
            low = x_start
        case '-x':
            high = x_start
            low = x_start - 1998
        case '+y':
            high = y_start + 1998
            low = y_start
        case '-y':
            high = y_start
            low = y_start - 1998
        case _:
            raise ValueError(f'Invalid direction: {direction}')
    return binary_search(high, low)


def find_chunk(x_start: int, y_start: int) -> Dict[str, int]:
    """

    :param x_start:
    :param y_start:
    :return Tuple[tuple, tuple]:
    """

    border_right = find_border(x_start, y_start, '+x')
    border_left = find_border(x_start, y_start, '-x')
    border_bot = find_border(x_start, y_start, '-y')
    border_top = find_border(x_start, y_start, '+y')
    return {'border_top': border_top, 'border_bot': border_bot,
            'border_left': border_left, 'border_right': border_right}


def check_cell(x_point: int, y_point: int) -> None:
    # print(f'Checking cell at ({x_point}, {y_point})')
    if find_sum_of_two_digits(x_point, y_point) <= MAX_VALUE:
        if (x_point, y_point + 1) in dict_of_points \
                or (x_point, y_point - 1) in dict_of_points \
                or (x_point + 1, y_point) in dict_of_points \
                or (x_point - 1, y_point) in dict_of_points:
            dict_of_points[(x_point, y_point)] = True


def check_quarter_of_chunk(quarter, border_points: Dict[str, int], x_start: int, y_start: int) -> None:
    print('check quarter', quarter)
    if quarter == 'I':
        if MAX_VALUE >= find_sum_of_two_digits(x_start, y_start + 1):
            y_start = y_start + 1
            direction = (1, 1)
        else:
            border_points['border_top'] = y_start
            return None
    elif quarter == 'II':
        if MAX_VALUE >= find_sum_of_two_digits(x_start - 1, y_start):
            x_start = x_start - 1
            direction = (-1, 1)
        else:
            border_points['border_left'] = x_start
            return None
    elif quarter == 'III':
        if MAX_VALUE >= find_sum_of_two_digits(x_start, y_start - 1):
            y_start = y_start - 1
            direction = (-1, -1)
        else:
            border_points['border_bot'] = y_start
            return None
    elif quarter == 'IV':
        if MAX_VALUE >= find_sum_of_two_digits(x_start + 1, y_start):
            x_start = x_start + 1
            direction = (1, -1)
        else:
            border_points['border_right'] = x_start
            return None
    else:
        raise ValueError(f'Invalid quarter: {quarter}')
    y_point = y_start
    x_point = x_start
    while True:
        if y_point > border_points['border_top'] or y_point < border_points['border_bot']:
            break
        check_cell(x_point, y_point)
        x_point = x_point + direction[0]
        if x_point > border_points['border_right'] or x_point < border_points['border_left']:
            y_point += direction[1]
            x_point = x_start


if MAX_VALUE >= find_sum_of_two_digits(X_START, Y_START):
    dict_of_points[(X_START, Y_START)] = True
else:
    raise ValueError(f'Invalid points of start: ({X_START} {Y_START})')

border_points = find_chunk(X_START, Y_START)
pprint(border_points)

quarters = ('I', 'II', 'III', 'IV')
for quarter in quarters:
    check_quarter_of_chunk(quarter, border_points, X_START, Y_START)
print(len(dict_of_points))

# x_points = []
# y_points = []
# for key in dict_of_points:
#     x_points.append(key[0])
#     y_points.append(key[1])
#
# plt.scatter(x_points, y_points)
# plt.show()
