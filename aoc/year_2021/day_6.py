from collections import Counter

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    def __init__(self, inp: Input):
        self.fishes = Counter(map(int, inp.get_lines()[0].split(",")))

    def simulate(self, days):
        fishes = dict(self.fishes)
        for _ in range(days):
            fishes = {(fish - 1): count for fish, count in fishes.items()}
            if born := fishes.pop(-1) if -1 in fishes else 0:
                fishes[8] = born
                fishes[6] = fishes.get(6, 0) + born
        return sum(fishes.values())

    def part_a(self):
        return self.simulate(80)

    def part_b(self):
        return self.simulate(256)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
