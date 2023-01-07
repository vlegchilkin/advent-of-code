import inspect
import os
import re
from pathlib import Path
from typing import Union, Iterator, Any, Callable, Optional

import numpy as np
from addict import Dict
from ttp import ttp

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
