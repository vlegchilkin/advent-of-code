import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        self.pairs = inp.get_lists("{{a0|to_int}}-{{a1|to_int}},{{b0|to_int}}-{{b1|to_int}}")

    def part_a(self):
        overlap = 0
        for a_, _a, b_, _b in self.pairs:
            overlap += (a_ <= b_ and _b <= _a) or (b_ <= a_ and _a <= _b)
        return overlap

    def part_b(self):
        intersect = 0
        for a_, _a, b_, _b in self.pairs:
            intersect += (a_ <= b_ <= _a) or (b_ <= a_ <= _b)
        return intersect


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
