import collections
import re
from typing import Callable

import pytest

from aoc import Input, get_puzzles, PuzzleData, t_koef, t_sum, XY, get_vector, split_to_steps


class Solution:
    def __init__(self, inp: Input):
        def parse(line):
            n = list(map(int, re.findall(r"\d+", line)))
            return [(n[0], n[1]), (n[2], n[3])]

        self.lines = inp.get_lines(parse)

    def count_intersections(self, filter_func: Callable[[XY], bool] = None):
        ar = collections.defaultdict(int)
        for a, b in self.lines:
            vector = get_vector(a, b)
            if filter_func and not filter_func(vector):
                continue
            step, count = split_to_steps(vector)
            for i in range(count + 1):
                ar[t_sum(a, t_koef(i, step))] += 1
        return sum(x > 1 for x in ar.values())

    def part_a(self):
        return self.count_intersections(lambda v: v[0] * v[1] == 0)

    def part_b(self):
        return self.count_intersections()


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
