import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2017Day1(Solution):
    def __init__(self, inp: Input):
        self.data = [int(c) for c in inp.get_text().strip()]

    def solve(self, offset=1):
        n = len(self.data)
        return sum([self.data[i] for i in range(n) if self.data[i] == self.data[(i + offset) % n]])

    def part_a(self):
        return self.solve()

    def part_b(self):
        return self.solve(len(self.data) // 2)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day1)
