import statistics

import math
import pytest
from numpy import Inf

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2021Day7(Solution):
    def __init__(self, inp: Input):
        self.crabs = [int(pos) for pos in inp.get_lines()[0].split(",")]

    def bruteforce(self, func) -> int:
        def fuel(x):
            return sum((func(abs(pos - x)) for pos in self.crabs))

        min_fuel = Inf
        for consumption in map(fuel, range(min(self.crabs), max(self.crabs) + 1)):
            if consumption > min_fuel:
                break
            min_fuel = consumption

        return min_fuel

    def part_a(self):
        median = math.ceil(statistics.median(self.crabs))
        stat_result = sum((abs(c - median) for c in self.crabs))

        bruteforce_result = self.bruteforce(lambda x: x)
        assert stat_result == bruteforce_result

        return stat_result

    def part_b(self):
        return self.bruteforce(lambda x: x * (x + 1) // 2)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2021Day7)
