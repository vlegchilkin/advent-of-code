from itertools import cycle

from aoc import Input


class Solution:
    def __init__(self, inp: Input):
        self.lines = [int(line) for line in inp.get_lines()]

    def part_a(self):
        return sum(self.lines)

    def part_b(self):
        current = 0
        freq = {current}
        for change in iter(cycle(self.lines)):
            if (current := current + change) in freq:
                break
            freq.add(current)
        return current


def test_challenge():
    solution = Solution(Input())
    assert solution.part_a() == 569
    assert solution.part_b() == 77666
