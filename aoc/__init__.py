import inspect
import os
import re
from enum import Enum
from pathlib import Path
from typing import Union, Iterator, Any, Tuple, Iterable, Callable, Optional, TypeAlias

import math
import numpy as np
from addict import Dict
from ttp import ttp

from aoc.tpl import t_sum, t_delta

RESOURCES_ROOT = Path(__file__).parent.parent / "resources"
DAY_SOURCE_REG = re.compile(r"^.*/year_(\d+)/day_(\d+)(_+)?.py$")


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


def dataclass_by_template(data_cls, text: str, ttp_template: str):
    return data_cls(**parse_with_template(text, ttp_template)[0])


def _resolve_year_day():
    for s in inspect.stack():
        if match := DAY_SOURCE_REG.match(s.filename):
            groups = match.groups()
            return int(groups[0]), int(groups[1])


def get_puzzles():
    result = []
    if not (period := _resolve_year_day()):
        return result
    year, day = period
    for root, dirs, file_names in sorted(os.walk(RESOURCES_ROOT / f"{year}" / "day" / f"{day}")):
        for file_name in sorted(file_names):
            if file_name.endswith(".out"):
                test_case = file_name[:-4]
                result.append(PuzzleData(test_case, year, day))
    return result


class Input:
    def __init__(self, test_case: Union[str, int] = "puzzle", year=None, day=None):
        if year is None:
            year, day = _resolve_year_day()
        with open(RESOURCES_ROOT / f"{year}" / "day" / f"{day}" / f"{test_case}.in", "r") as file:
            self._text = file.read()

    def get_lines(self, func=lambda x: x) -> list:
        return [func(line) for line in self._text.splitlines()]

    def get_iter(self) -> Iterator[str]:
        return iter(self.get_lines())

    def get_blocks(self, line_iter=None) -> list[list]:
        line_iter = line_iter or self.get_iter()
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

    def get_array(self, decoder: Optional[Callable[[str], Any]] = None, *, sep: str = None, lines=None) -> np.ndarray:
        lines = lines or self._text.splitlines()
        width = max(map(len, lines))
        lines = [line.ljust(width) for line in lines]

        def decode(line: str) -> list:
            characters = list(line) if not sep else line.split(sep)
            return [decoder(c) for c in characters] if decoder else characters

        return np.array([decode(line) for line in lines])

    def get_text(self) -> str:
        return self._text


class Output:
    def __init__(self, year: int, day: int, test_case: str):
        with open(RESOURCES_ROOT / f"{year}" / "day" / f"{day}" / f"{test_case}.out", "r") as file:
            self.a = file.readline().strip()
            self.b = file.read().strip()


class PuzzleData:
    def __init__(self, test_case: str, year: int = None, day: int = None):
        if year is None:
            year, day = _resolve_year_day()
        self.test_case = test_case
        self.inp = Input(test_case, year, day)
        self.out = Output(year, day, test_case)

    def check_solution(self, solution_class):
        solution = solution_class(self.inp)
        if hasattr(solution, "part_a_b"):
            res_a, res_b = solution.part_a_b()
        else:
            res_a = solution.part_a()
            res_b = solution.part_b()
        assert str(res_a).strip() == self.out.a
        assert str(res_b).strip() == self.out.b

    def __str__(self) -> str:
        return self.test_case


XY: TypeAlias = Tuple[int, int]
XYZ: TypeAlias = Tuple[int, int, int]

Line: TypeAlias = Tuple[XY, XY]


class D(XY, Enum):
    NORTH = (-1, 0)
    NORTH_EAST = (-1, 1)
    EAST = (0, 1)
    SOUTH_EAST = (1, 1)
    SOUTH = (1, 0)
    SOUTH_WEST = (1, -1)
    WEST = (0, -1)
    NORTH_WEST = (-1, -1)


D_DIAGONALS = (D.NORTH_EAST, D.SOUTH_EAST, D.SOUTH_WEST, D.NORTH_WEST)
D_BORDERS = (D.NORTH, D.SOUTH, D.WEST, D.EAST)
D_ALL = tuple(D)

D_TURNS = {
    D.EAST: {"R": D.SOUTH, "L": D.NORTH},
    D.SOUTH: {"R": D.WEST, "L": D.EAST},
    D.WEST: {"R": D.NORTH, "L": D.SOUTH},
    D.NORTH: {"R": D.EAST, "L": D.WEST},
}

D_OPPOSITE = {D.EAST: D.WEST, D.WEST: D.EAST, D.NORTH: D.SOUTH, D.SOUTH: D.NORTH}

D_MOVES = {
    "<": D.WEST,
    ">": D.EAST,
    "^": D.NORTH,
    "v": D.SOUTH,
}


class Spacer:
    def __init__(self, n, m, *, default_directions: Iterable[XY] = D_ALL):
        self.n = n
        self.m = m
        self.default_directions = D_ALL if default_directions is None else default_directions

    def get_links(
        self, from_pos, directions: Iterable[XY] = None, *, test: Callable[[XY], bool] = None
    ) -> Iterator[tuple]:
        if directions is None:
            directions = self.default_directions

        for direct in directions:
            to_pos = from_pos[0] + direct[0], from_pos[1] + direct[1]
            if not 0 <= to_pos[0] < self.n or not 0 <= to_pos[1] < self.m:
                continue
            if test and not test(to_pos):
                continue
            yield to_pos

    def move(self, pos: XY, direction: D, *, cyclic=True):
        next_pos = t_sum(pos, direction)
        if 0 <= next_pos[0] < self.n and 0 <= next_pos[1] < self.m:
            return next_pos
        else:
            if not cyclic:
                raise OverflowError("Got out of dimensions")

            x = next_pos[0] % self.n
            if x < 0:
                x += self.n

            y = next_pos[1] % self.m
            if y < 0:
                y += self.m

            return x, y


def dist(x, y, *, manhattan: bool = True) -> Union[int, float]:
    if manhattan:
        return sum(t_delta(x, y))
    else:
        return math.dist(x, y)
