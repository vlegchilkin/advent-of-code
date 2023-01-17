import itertools
import re

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Year2017Day15(ISolution):
    """2017/15: Dueling Generators"""

    def __init__(self, inp: Input):
        def parse(line):
            return int(re.match(r"^Generator (\w) starts with (\d+)$", line).groups()[-1])

        self.generators = [(start, factor) for start, factor in zip(inp.get_lines(parse), [16807, 48271])]

    @staticmethod
    def gen(value, factor, multiplier=1):
        while True:
            value = (value * factor) % 0x7FFFFFFF
            if value % multiplier == 0:
                yield value

    @staticmethod
    def count(gen_a, gen_b, rounds):
        return sum(1 for a, b in itertools.islice(zip(gen_a, gen_b), rounds) if a & 0xFFFF == b & 0xFFFF)

    def part_a(self):
        return self.count(
            self.gen(*self.generators[0]),
            self.gen(*self.generators[1]),
            40_000_000,
        )

    def part_b(self):
        return self.count(
            self.gen(*self.generators[0], 4),
            self.gen(*self.generators[1], 8),
            5_000_000,
        )


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day15)
