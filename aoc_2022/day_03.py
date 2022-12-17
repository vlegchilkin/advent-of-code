import math
import string
from functools import reduce

from aoc_2022 import Input


class Solution:
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


def test_simple():
    solution = Solution(Input(0))
    assert solution.part_a() == 157
    assert solution.part_b() == 70


def test_challenge():
    solution = Solution(Input())
    assert solution.part_a() == 8072
    assert solution.part_b() == 2567
