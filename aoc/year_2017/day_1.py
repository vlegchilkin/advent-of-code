from aoc import Input


class Solution:
    def __init__(self, inp: Input):
        self.data = [int(c) for c in inp.get_text().strip()]

    def solve(self, offset=1):
        n = len(self.data)
        return sum([self.data[i] for i in range(n) if self.data[i] == self.data[(i + offset) % n]])

    def part_a(self):
        return self.solve()

    def part_b(self):
        return self.solve(len(self.data) // 2)


def test_challenge():
    solution = Solution(Input())
    assert solution.part_a() == 1341
    assert solution.part_b() == 1348
