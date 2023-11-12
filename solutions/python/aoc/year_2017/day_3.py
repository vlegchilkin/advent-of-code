import itertools
import math

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.space import Spacer, C


class Year2017Day3(Solution):
    """2017/3: Spiral Memory"""

    def __init__(self, inp: Input):
        self.num = int(inp.get_lines()[0])

    def part_a(self):
        if (side := int(math.sqrt(self.num))) % 2:
            if side**2 < self.num:
                side += 2
        else:
            side += 1

        radius = (side - 1) // 2
        base = side**2
        while base >= self.num and side > 1:
            base -= side - 1

        middle = base + side // 2
        return abs(self.num - middle) + radius

    def part_b(self):
        spacer = Spacer(ranges=None, at={0j: 1})
        for r in itertools.count(1):
            path = [
                (complex(r - 1, r), C.NORTH),
                (complex(-r, r - 1), C.WEST),
                (complex(1 - r, -r), C.SOUTH),
                (complex(r, 1 - r), C.EAST),
            ]
            for base, direct in path:
                for offset in range(r * 2):
                    pos = base + offset * direct
                    spacer[pos] = sum(spacer[_pos] for _pos in spacer.links(pos))
                    if spacer[pos] > self.num:
                        return spacer[pos]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day3)
