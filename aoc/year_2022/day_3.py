import math
import string
from functools import reduce

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2022Day3(Solution):
    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    def sol(self, items) -> int:
        def f(s) -> int:
            return reduce(lambda x, y: x | y, [1 << string.ascii_letters.index(c) for c in s])

        return int(math.log(reduce(lambda x, y: x & y, [f(item) for item in items]), 2)) + 1

    def part_a(self):
        result = 0
        for line in self.lines:
            result += self.sol([line[: len(line) // 2], line[len(line) // 2 :]])
        return result

    def part_b(self):
        result = 0
        for i in range(0, len(self.lines), 3):
            result += self.sol(self.lines[i : i + 3])
        return result


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2022Day3)
