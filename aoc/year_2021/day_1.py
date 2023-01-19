import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2021Day1(Solution):
    def __init__(self, inp: Input):
        self.deeps = list(map(int, inp.get_iter()))

    def part_a(self):
        return sum(a < b for a, b in zip(self.deeps, self.deeps[1:]))

    def part_b(self):
        """Sliding windows has 2 elements in common (Axx < xxB, xx parts are the same), so have to compare only A & B"""
        return sum(a < b for a, b in zip(self.deeps, self.deeps[3:]))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2021Day1)
