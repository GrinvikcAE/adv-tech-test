from typing import Dict
from pprint import pprint
# import matplotlib.pyplot as plt

MAX_VALUE = 25
QUARTERS = ('I', 'II', 'III', 'IV')
dict_of_points = {}


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
    Rearranging digits to find the smallest number
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


def binary_search(high: int, low: int, x_start: int, y_start: int) -> int:
    """
    Binary search of number, where sum digits <= 25
    :param high:
    :param low:
    :param x_start:
    :param y_start:
    :return:
    """

    mid = (high + low) // 2
    if (low == x_start and high == x_start + 1998) or (low == x_start - 1998 and high == x_start):
        sum_of_digits = find_sum_of_two_digits(mid, y_start)
    else:
        sum_of_digits = find_sum_of_two_digits(mid, x_start)

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
        if (low == x_start and high == x_start + 1998) or (low == x_start - 1998 and high == x_start):
            sum_of_digits = find_sum_of_two_digits(mid, y_start)
        else:
            sum_of_digits = find_sum_of_two_digits(mid, x_start)
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
    return binary_search(high, low, x_start, y_start)


def find_chunk(x_start: int, y_start: int) -> Dict[str, int]:
    """
    Find a chunk of possible available cells
    :param x_start:
    :param y_start:
    :return: Dictionary with border values
    """

    border_right = find_border(x_start, y_start, '+x')
    border_left = find_border(x_start, y_start, '-x')
    border_bot = find_border(x_start, y_start, '-y')
    border_top = find_border(x_start, y_start, '+y')
    return {'border_top': border_top, 'border_bot': border_bot,
            'border_left': border_left, 'border_right': border_right}


def check_cell(x_point: int, y_point: int) -> None:
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
            return None
    elif quarter == 'II':
        if MAX_VALUE >= find_sum_of_two_digits(x_start - 1, y_start):
            x_start = x_start - 1
            direction = (-1, 1)
        else:
            return None
    elif quarter == 'III':
        if MAX_VALUE >= find_sum_of_two_digits(x_start, y_start - 1):
            y_start = y_start - 1
            direction = (-1, -1)
        else:
            return None
    elif quarter == 'IV':
        if MAX_VALUE >= find_sum_of_two_digits(x_start + 1, y_start):
            x_start = x_start + 1
            direction = (1, -1)
        else:
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


if __name__ == '__main__':
    try:
        x_start, y_start = map(int, input('Enter coordinates: X Y, or press Enter: ').split())
        print(x_start, y_start)
    except ValueError:
        x_start, y_start = 1000, 1000
    print(f'Coordinates: {x_start, y_start}')
    if MAX_VALUE >= find_sum_of_two_digits(x_start, y_start):
        dict_of_points[(x_start, y_start)] = True
    else:
        raise ValueError(f'Invalid points of start: ({x_start} {y_start})')

    border_points = find_chunk(x_start, y_start)

    for quarter in QUARTERS:
        check_quarter_of_chunk(quarter, border_points, x_start, y_start)
    print(len(dict_of_points))

    # 1000 1000 - 141258

    # x_points = []
    # y_points = []
    # for key in dict_of_points:
    #     x_points.append(key[0])
    #     y_points.append(key[1])
    #
    # plt.scatter(x_points, y_points)
    # plt.show()
