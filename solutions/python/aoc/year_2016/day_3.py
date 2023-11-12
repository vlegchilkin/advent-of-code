import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2016Day3(Solution):
    def __init__(self, inp: Input):
        self.triangles = inp.get_matrix(5, decoder=int)

    @staticmethod
    def is_triangle(triangle):
        s = sorted(triangle)
        return s[0] + s[1] > s[2]

    def part_a(self):
        return sum(map(self.is_triangle, self.triangles))

    def part_b(self):
        return sum(
            self.is_triangle(t) for g in range(0, len(self.triangles), 3) for t in zip(*self.triangles[g : g + 3])
        )


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day3)
