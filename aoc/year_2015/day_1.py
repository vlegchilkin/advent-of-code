from aoc import Input


class Solution:
    def __init__(self, inp: Input):
        self.data = [1 if c == "(" else -1 for c in inp.get_text()]

    def part_a(self):
        return sum(self.data)

    def part_b(self):
        floor = 0
        i = 0
        while floor != -1:
            floor += self.data[i]
            i += 1
        return i


def test_challenge():
    solution = Solution(Input())
    assert solution.part_a() == 280
    assert solution.part_b() == 1797
