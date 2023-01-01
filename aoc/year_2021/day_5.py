import re
from typing import Callable

import pytest

from aoc import Input, get_puzzles, PuzzleData, Spacer, t_koef, t_sum, XY


class Solution:
    def __init__(self, inp: Input):
        def parse(line):
            n = list(map(int, re.findall(r"\d+", line)))
            return [(n[0], n[1]), (n[2], n[3])]

        self.lines = inp.get_lines(parse)
        self.spacer = Spacer.build([point for line in self.lines for point in line])

    def count_intersections(self, filter_func: Callable[[XY], bool] = None):
        ar = self.spacer.new_array(0)
        for pos, direction in Spacer.lines_to_vectors(self.lines):
            if filter_func and not filter_func(direction):
                continue
            step, count = Spacer.to_direction_steps(direction)
            for i in range(count + 1):
                ar[t_sum(pos, t_koef(i, step))] += 1
        return len(ar[ar > 1])

    def part_a(self):
        return self.count_intersections(lambda v: v[0] * v[1] == 0)

    def part_b(self):
        return self.count_intersections()


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
