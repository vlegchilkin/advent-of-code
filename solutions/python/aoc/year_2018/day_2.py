import itertools
import math
from collections import Counter

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2018Day2(Solution):
    """2018/2: Inventory Management System"""

    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    def part_a(self):
        counts = {2: 0, 3: 0}
        for line in self.lines:
            c = Counter(line)
            for k in counts:
                if k in c.values():
                    counts[k] += 1
        return math.prod(counts.values())

    def part_b(self):
        for a, b in itertools.combinations(self.lines, 2):
            if len(diff := [i for i, (_a, _b) in enumerate(zip(a, b)) if _a != _b]) == 1:
                return a[: diff[0]] + a[diff[0] + 1 :]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day2)
