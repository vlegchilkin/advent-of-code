import re

import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        self.row, self.column = map(int, re.findall(r"\d+", inp.get_text()))

    def part_a(self):
        def gen(c=20151125):
            while True:
                yield c
                c = c * 252533 % 33554393

        it = gen()
        for i in range(self.row + self.column - 1):
            for k in range(i, -1, -1):
                x = next(it)
                if (k == self.row - 1) and (i - k == self.column - 1):
                    return x

    def part_b(self):
        return ""


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
