import inspect
import math
import re
from enum import Enum

import numpy as np
from pathlib import Path
from typing import Union, Iterator, Any, Tuple, Iterable, Callable
from addict import Dict

from ttp import ttp

RESOURCES_ROOT = Path(__file__).parent / "resources"
DAY_SOURCE_REG = re.compile(r"^.*day_(\d+)(_)?.py$")


def to_str_list(data, sep=","):
    return data.split(sep), None


def to_int_list(data, sep=","):
    return [int(el) for el in data.split(sep)], None


def to_optional_int(data, no_value="old"):
    if data == no_value:
        return None, None

    return int(data), None


def parse_with_template(text: str, ttp_template: str) -> list[Dict]:
    parser = ttp(data=text, template=ttp_template)
    parser.add_function(to_int_list, scope="match")
    parser.add_function(to_str_list, scope="match")
    parser.add_function(to_optional_int, scope="match")
    parser.parse()
    objects = parser.result(structure="flat_list")
    return [Dict(obj) for obj in objects]


class Input:
    def __init__(self, test_case: Union[str, int] = "puzzle"):
        caller_filename = inspect.stack()[1].filename
        day = DAY_SOURCE_REG.match(caller_filename).groups()[0]
        with open(RESOURCES_ROOT / day / f"{test_case}.in", "r") as file:
            self._text = file.read()

    def get_lines(self) -> list:
        return self._text.splitlines()

    def get_iter(self) -> Iterator[str]:
        return iter(self.get_lines())

    def get_blocks(self) -> list[list]:
        line_iter = self.get_iter()
        blocks = []
        while line := next(line_iter, None):
            block = []
            while line:
                block.append(line)
                line = next(line_iter, None)
            blocks.append(block)
        return blocks

    def get_objects(self, ttp_template: str) -> list[Dict]:
        return parse_with_template(self._text, ttp_template)

    def get_lists(self, ttp_template: str) -> list[list[Any]]:
        objects = self.get_objects(ttp_template)
        return [list(o.values()) for o in objects]

    def get_array(self, sep: str = None) -> (np.ndarray, Tuple):
        lines = self._text.splitlines()
        array = np.array([list(line) if not sep else line.split(sep) for line in lines])
        return array, array.shape

    def get_text(self) -> str:
        return self._text


class Direction(Tuple, Enum):
    NORTH = (-1, 0)
    NORTH_EAST = (-1, 1)
    EAST = (0, 1)
    SOUTH_EAST = (1, 1)
    SOUTH = (1, 0)
    SOUTH_WEST = (1, -1)
    WEST = (0, -1)
    NORTH_WEST = (-1, -1)


D_DIAGONALS = (Direction.NORTH_EAST, Direction.SOUTH_EAST, Direction.SOUTH_WEST, Direction.NORTH_WEST)
D_BORDERS = (Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST)
D_ALL = tuple(Direction)


class Spacer:
    def __init__(
        self, south, east, north_inclusive=0, west_inclusive=0, *, default_directions: Iterable[tuple] = D_ALL
    ):
        self.south = south
        self.east = east
        self.north_inclusive = north_inclusive
        self.west_inclusive = west_inclusive
        self.default_directions = D_ALL if default_directions is None else default_directions

    def get_links(
        self, from_pos, directions: Iterable[tuple] = None, *, test: Callable[[tuple], bool] = None
    ) -> Iterator[tuple]:
        if directions is None:
            directions = self.default_directions

        for direct in directions:
            to_pos = from_pos[0] + direct[0], from_pos[1] + direct[1]
            if not self.north_inclusive <= to_pos[0] < self.south or not self.west_inclusive <= to_pos[1] < self.east:
                continue
            if test and not test(to_pos):
                continue
            yield to_pos

    def iter(self, test: Callable[[tuple], bool] = None) -> Iterator[tuple]:
        for i in range(self.north_inclusive, self.south):
            for j in range(self.west_inclusive, self.east):
                if test and not test((i, j)):
                    continue
                yield i, j

    def new_array(self, fill_value, *, dtype=int):
        return np.full(
            shape=(self.south, self.east),
            fill_value=fill_value,
            dtype=dtype,
        )


def dist(x, y, *, manhattan: bool = True) -> Union[int, float]:
    if manhattan:
        return sum(t_delta(x, y))
    else:
        return math.dist(x, y)


def t_delta(x, y):
    match len(x):
        case 1:
            return abs(x - y)
        case 2:
            return abs(x[0] - y[0]), abs(x[1] - y[1])
        case 3:
            return abs(x[0] - y[0]), abs(x[1] - y[1]), abs(x[2] - y[2])
        case _:
            return tuple(abs(xx - yy) for xx, yy in zip(x, y))  # slow


def t_sum(x, y):
    match len(x):
        case 1:
            return x + y
        case 2:
            return x[0] + y[0], x[1] + y[1]
        case 3:
            return x[0] + y[0], x[1] + y[1], x[2] + y[2]
        case _:
            return tuple(map(sum, zip(x, y)))  # slow


def t_inside_array(pos, n):
    """is positions within dimension"""
    return (0 <= pos[0] < n[0]) and (0 <= pos[1] < n[1]) and (0 <= pos[2] < n[2])


def t_inside(pos, limits):
    """is positions within dimension"""
    return (
        (limits[0][0] <= pos[0] <= limits[1][0])
        and (limits[0][1] <= pos[1] <= limits[1][1])
        and (limits[0][2] <= pos[2] <= limits[1][2])
    )


def t_minmax(items):
    if len(items) == 0:
        return None

    match len(next(iter(items))):
        case 1:
            return min(items), max(items)
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
