import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    def __init__(self, inp: Input):
        self.masses = [int(line) for line in inp.get_lines()]

    @staticmethod
    def fuel(mass) -> int:
        if (r := mass // 3 - 2) > 0:
            return r + Solution.fuel(r)
        return 0

    def part_a(self):
        return sum([mass // 3 - 2 for mass in self.masses])

    def part_b(self):
        return sum([self.fuel(mass) for mass in self.masses])


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
