import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        self.deeps = [int(line) for line in inp.get_lines()]

    def part_a(self):
        result = 0
        for i in range(1, len(self.deeps)):
            result += self.deeps[i] > self.deeps[i - 1]
        return result

    def part_b(self):
        result = 0
        for i in range(3, len(self.deeps)):
            result += sum(self.deeps[i - 2 : i + 1]) > sum(self.deeps[i - 3 : i])
        return result


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
