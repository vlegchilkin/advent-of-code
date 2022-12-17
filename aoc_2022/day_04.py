from aoc_2022 import Input


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


def test_simple():
    solution = Solution(Input(0))
    assert solution.part_a() == 2
    assert solution.part_b() == 4


def test_challenge():
    solution = Solution(Input())
    assert solution.part_a() == 466
    assert solution.part_b() == 865
