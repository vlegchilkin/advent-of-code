from itertools import cycle

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Year2018Day1(ISolution):
    def __init__(self, inp: Input):
        self.lines = [int(line) for line in inp.get_lines()]

    def part_a(self):
        return sum(self.lines)

    def part_b(self):
        current = 0
        freq = {current}
        for change in iter(cycle(self.lines)):
            if (current := current + change) in freq:
                break
            freq.add(current)
        return current


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day1)
