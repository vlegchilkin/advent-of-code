import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
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


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
