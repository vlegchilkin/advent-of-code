import string

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2023Day1(Solution):
    """2023/1: Trebuchet?!"""

    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    def part_a(self):
        total = 0
        for line in self.lines:
            first = last = None
            for c in line:
                if c in string.digits:
                    last = int(c)
                    first = last if first is None else first
            total += first * 10 + last
        return total

    def part_b(self):
        nums = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}

        def decode(line: str) -> int:
            first = last = None
            for start, c in enumerate(line):
                if c in string.digits:
                    last = int(c)
                    first = last if first is None else first
                else:
                    for sub, val in nums.items():
                        if line.startswith(sub, start):
                            last = val
                            first = last if first is None else first
                            break
            return first * 10 + last

        return sum(map(decode, self.lines))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2023Day1)
