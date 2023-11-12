import re

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.space import Spacer, minmax


class Year2018Day10(Solution):
    """2018/10: The Stars Align"""

    def __init__(self, inp: Input):
        def parse(line):
            g = tuple(map(int, re.findall(r"-?\d+", line)))
            return (g[0], g[1]), (g[2], g[3])

        self.lights = inp.get_lines(parse)

    def part_a_b(self):
        lights = [(complex(p[1], p[0]), complex(v[1], v[0])) for p, v in self.lights]
        for s in range(0, 100_000):  # 100k limit to avoid an infinite loop
            mm = minmax([a for a, b in lights])
            if mm[1].real - mm[0].real == 9:  # characters height is 10
                spacer = Spacer(ranges=None, at={a: "#" for a, b in lights})
                return str(spacer), s
            lights = [(p + v, v) for p, v in lights]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day10)
