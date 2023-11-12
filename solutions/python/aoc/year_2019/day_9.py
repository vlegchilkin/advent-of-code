import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.year_2019 import IntcodeComputer


class Year2019Day9(Solution):
    """2019/9: Sensor Boost"""

    def __init__(self, inp: Input):
        self.instructions = list(map(int, inp.get_text().split(",")))

    def part_a(self):
        computer = IntcodeComputer(self.instructions)
        return computer.run([1])[0]

    def part_b(self):
        computer = IntcodeComputer(self.instructions)
        return computer.run([2])[0]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day9)
