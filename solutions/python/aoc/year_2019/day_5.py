import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.year_2019 import IntcodeComputer


class Year2019Day5(Solution):
    """2019/5: Sunny with a Chance of Asteroids"""

    def __init__(self, inp: Input):
        self.instructions = list(map(int, inp.get_text().split(",")))

    def part_a(self):
        buffer = self.instructions.copy()
        return IntcodeComputer(buffer).run([1])[-1]

    def part_b(self):
        buffer = self.instructions.copy()
        return IntcodeComputer(buffer).run([5])[-1]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day5)
