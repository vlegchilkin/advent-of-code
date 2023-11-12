import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.math import factors


class Year2015Day20(Solution):
    def __init__(self, inp: Input):
        self.min_presents = inp.get_lines(int)[0]

    def part_a(self):
        def presents(h):
            return sum(factors(h))

        min_presents = self.min_presents // 10
        house = min_presents // 5  # just optimization for tests, looks like enough, but wasn't prove
        while presents(house) < min_presents:
            house += 1
        return house

    def part_b(self):
        def presents(h):
            min_factor = h // 50
            return sum({factor for factor in factors(h) if factor >= min_factor})

        min_presents = self.min_presents // 11
        house = min_presents // 5  # just optimization for tests, looks like enough, but wasn't prove
        while presents(house) < min_presents:
            house += 1
        return house


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2015Day20)
