import math
from typing import Union


def t_ranges(items):
    mm = t_minmax(items)
    match len(next(iter(items))):
        case 1:
            return mm[0], mm[1]
        case 2:
            return (mm[0][0], mm[1][0] + 1), (mm[0][1], mm[1][1] + 1)
        case 3:
            return (mm[0][0], mm[1][0] + 1), (mm[0][1], mm[1][1] + 1), (mm[0][2], mm[1][2] + 1)
        case _:
            raise ValueError("Not implemented for dimension")


def t_minmax(items):
    if len(items) == 0:
        return None

    match len(next(iter(items))):
        case 1:
            return min(items[0]), max(items[0])
        case 2:
            return (
                (min([item[0] for item in items]), min([item[1] for item in items])),
                (max([item[0] for item in items]), max([item[1] for item in items])),
            )
        case 3:
            return (
                (min([item[0] for item in items]), min([item[1] for item in items]), min([item[2] for item in items])),
                (max([item[0] for item in items]), max([item[1] for item in items]), max([item[2] for item in items])),
            )
        case _:
            raise ValueError("Not implemented for dimension")


def t_inside(pos: tuple, limits: tuple[tuple, tuple]):
    """is positions within dimension"""
    match len(pos):
        case 1:
            return limits[0][0] <= pos[0] <= limits[1][0]
        case 2:
            return (limits[0][0] <= pos[0] <= limits[1][0]) and (limits[0][1] <= pos[1] <= limits[1][1])
        case 3:
            return (
                (limits[0][0] <= pos[0] <= limits[1][0])
                and (limits[0][1] <= pos[1] <= limits[1][1])
                and (limits[0][2] <= pos[2] <= limits[1][2])
            )
        case _:
            raise ValueError("Not implemented for dimension")


def t_add_pos(t, pos, value):
    return tuple(c if idx != pos else c + value for idx, c in enumerate(t))


def t_replace(t, pos, value):
    return tuple(c if idx != pos else value for idx, c in enumerate(t))


def t_pop_left(t):
    for i, v in enumerate(t):
        if v:
            return t_add_pos(t, i, -v)
    return t


def t_push_left(t, value):
    for i, v in enumerate(t):
        if v:
            return t_add_pos(t, i - 1, value)
    return t_add_pos(t, len(t) - 1, value)


def t_koef(x, y: tuple):
    match len(y):
        case 1:
            return int(x * y[0])
        case 2:
            return int(x * y[0]), int(x * y[1])
        case 3:
            return int(x * y[0]), int(x * y[1]), int(x * y[2])
        case 4:
            return int(x * y[0]), int(x * y[1]), int(x * y[2]), int(x * y[3])
        case _:
            raise ValueError("not implemented")


def t_sub(x: tuple, y: tuple):
    match len(x):
        case 1:
            return x[0] - y[0]
        case 2:
            return x[0] - y[0], x[1] - y[1]
        case 3:
            return x[0] - y[0], x[1] - y[1], x[2] - y[2]
        case 4:
            return x[0] - y[0], x[1] - y[1], x[2] - y[2], x[3] - y[3]
        case _:
            return t_sum(x, t_koef(-1, y))  # slow


def t_sum(x: tuple, y: tuple):
    match len(x):
        case 1:
            return x[0] + y[0]
        case 2:
            return x[0] + y[0], x[1] + y[1]
        case 3:
            return x[0] + y[0], x[1] + y[1], x[2] + y[2]
        case 4:
            return x[0] + y[0], x[1] + y[1], x[2] + y[2], x[3] + y[3]
        case _:
            return tuple(map(sum, zip(x, y)))  # slow


def t_delta(x, y):
    match len(x):
        case 1:
            return abs(x - y)
        case 2:
            return abs(x[0] - y[0]), abs(x[1] - y[1])
        case 3:
            return abs(x[0] - y[0]), abs(x[1] - y[1]), abs(x[2] - y[2])
        case 4:
            return abs(x[0] - y[0]), abs(x[1] - y[1]), abs(x[2] - y[2]), abs(x[3] - y[3])
        case _:
            return tuple(abs(xx - yy) for xx, yy in zip(x, y))  # slow


def t_dist(x, y, *, manhattan: bool = True) -> Union[int, float]:
    if manhattan:
        return sum(t_delta(x, y))
    else:
        return math.dist(x, y)
