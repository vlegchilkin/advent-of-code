import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.year_2016 import assembunny


class Year2016Day12(Solution):
    """2016/12: Leonardo's Monorail"""

    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    def part_a(self):
        return assembunny(self.lines)[0]["a"]

    def part_b(self):
        return assembunny(self.lines, c=1)[0]["a"]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day12)
