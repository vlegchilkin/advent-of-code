import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.math import factors
from solutions.python.aoc.year_2017.day_18 import Year2017Day18


class Year2017Day23(Solution):
    """2017/23: Coprocessor Conflagration"""

    def __init__(self, inp: Input):
        self.computer = Year2017Day18(inp)

    def part_a(self):
        regs = {reg: 0 for reg in "abcdefgh"}
        counter = 0

        def interceptor(idx, cmd, args):
            if cmd == "mul":
                nonlocal counter
                counter += 1

        self.computer.run(regs, interceptor=interceptor)
        return counter

    def part_b(self):
        """Count prime numbers in a range with step 17"""
        regs = {reg: int(reg == "a") for reg in "abcdefgh"}

        # run first 7 steps to get scan range from registers: b..c
        self.computer.run(regs, interceptor=lambda i, c, a: -1 if i == 8 else None)

        h = 0
        for n in range(regs["b"], regs["c"] + 1, 17):
            if len(factors(n)) > 2:
                h += 1
        return h


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day23)
