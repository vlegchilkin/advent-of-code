import itertools

import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        self.entries = [int(line) for line in inp.get_lines()]

    def part_a(self):
        for a, b in itertools.combinations(self.entries, 2):
            if a + b == 2020:
                return a * b

    def part_b(self):
        for a, b, c in itertools.combinations(self.entries, 3):
            if a + b + c == 2020:
                return a * b * c


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
