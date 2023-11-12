import itertools

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.year_2016 import assembunny


class Year2016Day25(Solution):
    """2016/25: Clock Signal"""

    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    def part_a(self):
        for a in itertools.count():
            _, out = assembunny(self.lines, a=a, out_limit=10)
            if out == [0, 1] * 5:
                return a


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day25)
