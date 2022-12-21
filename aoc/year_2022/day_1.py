from aoc import Input


class Solution:
    def __init__(self, inp: Input):
        sums, capacities = 0, []
        for line in inp.get_lines():
            if line:
                sums += int(line)
            else:
                capacities.append(sums)
                sums = 0
        capacities.append(sums)
        self.top3 = sorted(capacities, reverse=True)[:3]

    def part_a(self):
        return self.top3[0]

    def part_b(self):
        return sum(self.top3)


def test_simple():
    solution = Solution(Input(0))
    assert solution.part_a() == 24000
    assert solution.part_b() == 45000


def test_puzzle():
    solution = Solution(Input())
    assert solution.part_a() == 72017
    assert solution.part_b() == 212520
