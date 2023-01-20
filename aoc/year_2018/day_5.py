import re
import string

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2018Day5(Solution):
    """2018/5: Alchemical Reduction"""

    def __init__(self, inp: Input):
        self.polymer = inp.get_lines()[0]

    @staticmethod
    def react(polymer):
        c = "|".join([f"{a}{b}|{b}{a}" for a, b in zip(string.ascii_lowercase, string.ascii_uppercase)])
        x_len = len(polymer)
        while len(polymer := re.sub(c, "", polymer)) < x_len:
            x_len = len(polymer)
        return x_len

    def part_a(self):
        return self.react(self.polymer)

    def part_b(self):
        return min(
            self.react(re.sub(rf"{a}|{b}", "", self.polymer))
            for a, b in zip(string.ascii_lowercase, string.ascii_uppercase)
        )


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day5)
