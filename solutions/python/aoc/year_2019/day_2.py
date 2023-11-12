import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.year_2019 import IntcodeComputer


class Year2019Day2(Solution):
    """2019/2: 1202 Program Alarm"""

    def __init__(self, inp: Input):
        self.instructions = list(map(int, inp.get_text().split(",")))

    def run(self, noun, verb):
        buffer = self.instructions.copy()
        buffer[1], buffer[2] = noun, verb
        computer = IntcodeComputer(buffer)
        computer.run()
        return computer.memory[0]

    def part_a(self):
        return self.run(12, 2)

    def part_b(self):
        required = 19690720
        for noun in range(100):
            for verb in range(100):
                if self.run(noun, verb) == required:
                    return noun * 100 + verb


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day2)
