import collections as cl

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2016Day6(Solution):
    """2016/6: Signals and Noise"""

    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    def decode(self, pos):
        result = ""
        for letters in zip(*self.lines):
            letter_counts = cl.Counter(letters).items()
            result += sorted(letter_counts, key=lambda item: item[1])[pos][0]
        return result

    def part_a(self):
        return self.decode(-1)

    def part_b(self):
        return self.decode(0)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day6)
