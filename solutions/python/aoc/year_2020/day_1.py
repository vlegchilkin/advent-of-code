import itertools

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2020Day1(Solution):
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
    pd.check_solution(Year2020Day1)
