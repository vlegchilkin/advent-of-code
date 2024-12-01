import re
import itertools as it
import collections as cl
import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2024Day1(Solution):
    """2024/1: Historian Hysteria"""

    def __init__(self, inp: Input):
        numbers = map(int, re.findall(r"\d+", inp.get_text()))
        self.pairs = list(it.batched(numbers, 2))

    def part_a_b(self):
        first, second = zip(*self.pairs)
        part_a = sum(abs(f - s) for f, s in zip(sorted(first), sorted(second)))

        second_counter = cl.Counter(second)
        part_b = sum(number * second_counter[number] for number in first)
        return part_a, part_b

@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2024Day1)
