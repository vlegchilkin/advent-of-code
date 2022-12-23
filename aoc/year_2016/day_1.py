from aoc import Input, D, t_sum, t_koef, dist

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
            for step in range(move[1]):
                pos = t_sum(pos, direction)
                if pos in visited:
                    return dist(start, pos)
                visited.add(pos)


def test_challenge():
    solution = Solution(Input())
    assert solution.part_a() == 239
    assert solution.part_b() == 141
