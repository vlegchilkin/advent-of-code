import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution
from aoc.space import C, c_dist, C_TURNS


class Solution(ISolution):
    def __init__(self, inp: Input):
        self.moves = [(m[0], int(m[1:])) for m in inp.get_text().split(", ")]

    def part_a(self):
        start = pos = 0j
        direction = C.NORTH
        for move in self.moves:
            direction = C_TURNS[direction][move[0]]
            pos += move[1] * direction
        return c_dist(start, pos)

    def part_b(self):
        start = pos = 0j
        visited = {start}
        direction = C.NORTH
        for move in self.moves:
            direction = C_TURNS[direction][move[0]]
            for _ in range(move[1]):
                pos += direction
                if pos in visited:
                    return c_dist(start, pos)
                visited.add(pos)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
