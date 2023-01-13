import itertools

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution
from aoc.year_2016 import assembunny


class Solution(ISolution):
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
    pd.check_solution(Solution)
