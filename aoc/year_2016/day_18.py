import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution
from aoc.space import Spacer, C
import numpy as np


class Solution(ISolution):
    """2016/18: Like a Rogue"""

    def __init__(self, inp: Input):
        self.first_row = np.array([v == "^" or None for v in inp.get_lines()[0]])

    def count_traps(self, rows):
        spacer = Spacer.build(self.first_row, ranges=((0, 0), (rows, len(self.first_row))))
        for pos in spacer.iter(test=lambda p: p.real > 0):
            if spacer.at.get(pos + C.NORTH_WEST) != spacer.at.get(pos + C.NORTH_EAST):
                spacer[pos] = True

        return spacer.n * spacer.m - len(spacer)

    def part_a(self):
        return self.count_traps(40)

    def part_b(self):
        return self.count_traps(400000)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
