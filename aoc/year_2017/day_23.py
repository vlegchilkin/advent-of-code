import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution
from aoc.math import factors
from aoc.year_2017.day_18 import Year2017Day18


class Year2017Day23(ISolution):
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
        start = 57 * 100 + 100_000
        h = 0
        for n in range(start, start + 17_000 + 1, 17):
            if len(factors(n)) > 2:
                h += 1
        return h


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day23)
