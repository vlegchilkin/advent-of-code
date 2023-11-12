import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.year_2016 import assembunny


class Year2016Day23(Solution):
    """2016/23: Safe Cracking"""

    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    @staticmethod
    def interceptor(index, regs, _) -> int:
        if index == 2:
            regs["a"] *= regs["b"]
            regs["b"] -= 1
            regs["c"] = regs["d"] = 0
            return 10
        return index

    def part_a(self):
        return assembunny(self.lines, a=7, interceptor=self.interceptor)[0]["a"]

    def part_b(self):
        return assembunny(self.lines, a=12, interceptor=self.interceptor)[0]["a"]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day23)
