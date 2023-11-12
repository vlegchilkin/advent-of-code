import re

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.space import Spacer


class Year2016Day8(Solution):
    """2016/8: Two-Factor Authentication"""

    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    def part_a_b(self):
        spacer = Spacer((6, 50))
        for line in self.lines:
            cmd, _, args = line.partition(" ")
            a, b = map(int, re.findall(r"\d+", args))
            match cmd:
                case "rect":
                    for i in range(b):
                        for j in range(a):
                            spacer[complex(i, j)] = "#"
                case "rotate":
                    if args.startswith("row"):
                        spacer.rotate(b, row=a)
                    else:
                        spacer.rotate(b, col=a)
                case _:
                    raise ValueError(f"Non-supported command {cmd}")
        return sum(v == "#" for v in spacer.at.values()), str(spacer)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day8)
