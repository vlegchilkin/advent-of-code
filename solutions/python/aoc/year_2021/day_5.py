import collections
import re
from numbers import Complex
from typing import Callable

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import split_to_steps


class Year2021Day5(Solution):
    def __init__(self, inp: Input):
        def parse(line):
            n = list(map(int, re.findall(r"\d+", line)))
            return complex(n[0], n[1]), complex(n[2], n[3])

        self.lines = inp.get_lines(parse)

    def count_intersections(self, filter_func: Callable[[Complex], bool] = None):
        space = collections.defaultdict(int)
        for a, b in self.lines:
            step, count = split_to_steps(b - a)
            if filter_func and not filter_func(step):
                continue

            for i in range(count + 1):
                space[a + i * step] += 1

        return sum(x > 1 for x in space.values())

    def part_a(self):
        return self.count_intersections(lambda v: v.real * v.imag == 0)

    def part_b(self):
        return self.count_intersections()


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2021Day5)
