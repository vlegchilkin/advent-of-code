import pytest

from aoc import Input, D, dist, get_puzzles, PuzzleData
from aoc.tpl import t_koef, t_sum

ROTATE = {
    D.NORTH: {"R": D.EAST, "L": D.WEST},
    D.SOUTH: {"R": D.WEST, "L": D.EAST},
    D.WEST: {"R": D.NORTH, "L": D.SOUTH},
    D.EAST: {"R": D.SOUTH, "L": D.NORTH},
}


class Solution:
    def __init__(self, inp: Input):
        self.moves = [(m[0], int(m[1:])) for m in inp.get_text().split(", ")]

    def part_a(self):
        start = pos = (0, 0)
        direction = D.NORTH
        for move in self.moves:
            direction = ROTATE[direction][move[0]]
            pos = t_sum(pos, t_koef(move[1], direction))
        return dist(start, pos)

    def part_b(self):
        start = pos = (0, 0)
        visited = {start}
        direction = D.NORTH
        for move in self.moves:
            direction = ROTATE[direction][move[0]]
            for _ in range(move[1]):
                pos = t_sum(pos, direction)
                if pos in visited:
                    return dist(start, pos)
                visited.add(pos)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
