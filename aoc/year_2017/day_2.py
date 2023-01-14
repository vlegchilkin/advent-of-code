import itertools
import re

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Year2017Day2(ISolution):
    """2017/2: Corruption Checksum"""

    def __init__(self, inp: Input):
        self.lines = inp.get_lines(lambda s: list(map(int, re.findall(r"\d+", s))))

    def part_a(self):
        return sum(max(line) - min(line) for line in self.lines)

    def part_b(self):
        return sum(b // a for line in self.lines for a, b in itertools.combinations(sorted(line), 2) if b % a == 0)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day2)
