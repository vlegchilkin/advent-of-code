from aoc_2022 import Input


class Solution:
    def __init__(self, inp: Input):
        self.line = inp.get_lines()[0]

    def find_unique(self, length) -> int:
        for i in range(length, len(self.line)):
            if len(set(self.line[i - length : i])) == length:
                return i

    def part_a(self):
        return self.find_unique(4)

    def part_b(self):
        return self.find_unique(14)


def test_simple():
    solution = Solution(Input(0))
    assert solution.part_a() == 7
    assert solution.part_b() == 19


def test_puzzle():
    solution = Solution(Input())
    assert solution.part_a() == 1625
    assert solution.part_b() == 2250
