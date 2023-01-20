import inspect
import os
import re
from abc import abstractmethod
from pathlib import Path
from typing import Union, Iterator, Any, Callable, Optional, Type, TypeVar

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


T = TypeVar("T")


class Input:
    def __init__(self, test_case: Union[str, int] = "puzzle", year=None, day=None):
        if year is None:
            year, day = _resolve_year_day()
        with open(RESOURCES_ROOT / f"{year}" / "day" / f"{day}" / f"{test_case}.in", "r") as file:
            self._text = file.read()

    def get_lines(self, func: Callable[[str], T] = lambda x: x) -> list[T]:
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

    def get_dc_list(self, ttp_template: str, dc_class: Type[T]) -> list[T]:
        return [dc_class(**d) for d in parse_with_template(self._text, ttp_template)]

    def get_lists(self, ttp_template: str) -> list[list[Any]]:
        objects = self.get_objects(ttp_template)
        return [list(o.values()) for o in objects]

    def _build_array(self, lines, decode):
        lines = lines or self._text.splitlines()
        width = max(map(len, lines))
        lines = [line.ljust(width) for line in lines]

        return np.array([decode(line) for line in lines])

    def get_matrix(self, size, decoder: Optional[Callable[[str], Any]] = None, *, lines=None) -> np.ndarray:
        def decode(line: str) -> list:
            xx = [line[i : i + size].strip() or None for i in range(0, len(line), size)]
            return [decoder(c) for c in xx] if decoder else xx

        return self._build_array(lines, decode)

    def get_array(self, decoder: Optional[Callable[[str], Any]] = None, *, sep: str = None, lines=None) -> np.ndarray:
        def decode(line: str) -> list:
            characters = list(line) if not sep else line.split(sep)
            return [decoder(c) for c in characters] if decoder else characters

        return self._build_array(lines, decode)

    def get_text(self) -> str:
        return self._text


class Output:
    def __init__(self, year: int, day: int, test_case: str):
        with open(RESOURCES_ROOT / f"{year}" / "day" / f"{day}" / f"{test_case}.out", "r") as file:
            self.a_b = file.read()

    @property
    def a(self):
        return self.a_b.split("\n")[0]

    @property
    def b(self):
        return "\n".join(self.a_b.split("\n")[1:]).strip()


class Solution:
    @abstractmethod
    def __init__(self, inp: Input):
        """
        :param inp: puzzle input data
        """

    def part_a(self) -> Any:
        return ""

    def part_b(self) -> Any:
        return ""

    def part_a_b(self) -> (Any, Any):
        return self.part_a(), self.part_b()


class PuzzleData:
    def __init__(self, test_case: str, year: int = None, day: int = None):
        if year is None:
            year, day = _resolve_year_day()
        self.test_case = test_case
        self.inp = Input(test_case, year, day)
        self.out = Output(year, day, test_case)

    def check_solution(self, solution_class: Type[Solution]):
        solution = solution_class(self.inp)
        res_a, res_b = solution.part_a_b()
        assert f"{str(res_a).strip()}\n{res_b}".strip() == self.out.a_b.strip()

    def __str__(self) -> str:
        return self.test_case
