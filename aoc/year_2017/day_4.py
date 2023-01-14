import itertools
from collections import Counter

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Year2017Day4(ISolution):
    """2017/4: High-Entropy Passphrases"""

    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    def part_a(self):
        counter = 0
        for line in self.lines:
            counter += not any(count for _, count in Counter(line.split(" ")).items() if count > 1)
        return counter

    def part_b(self):
        counter = 0
        for line in self.lines:
            letters = sorted([sorted(word) for word in line.split(" ")])
            counter += not any(a == b for a, b in itertools.pairwise(letters))
        return counter


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day4)
