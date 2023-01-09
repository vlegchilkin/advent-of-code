import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
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


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
