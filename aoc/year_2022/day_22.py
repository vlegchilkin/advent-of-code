import numpy as np

from aoc import Input, D, t_sum, Spacer, D_TURNS

SIDES = [D.EAST, D.SOUTH, D.WEST, D.NORTH]


class Cube:
    def __init__(self, pattern, data, portal_builder):
        self.sides = {}
        self.dim = len(data) // len(pattern)
        for off_i, v in enumerate(pattern):
            for off_j, c in enumerate(v):
                if not c:
                    continue
                self.sides[c] = (self.dim * off_i, self.dim * off_j)
        self.portals = portal_builder(data, self.dim, self.sides)

    def move(self, pos: tuple[int, int], direction: D) -> (tuple[int, int], D):
        return self.portals[pos][direction]


class Solution:
    def __init__(self, inp: Input, cube_pattern: list[list], portal_builder):
        area_data = []
        inp_iter = inp.get_iter()
        while line := next(inp_iter):
            area_data.append(list(line))

        shape = len(area_data), max([len(r) for r in area_data])
        self.area = np.full(shape, dtype=int, fill_value=0)
        for i, row in enumerate(area_data):
            for j, c in enumerate(row):
                self.area[i, j] = -1 if c == "." else 1 if c == "#" else 0

        self.cube = Cube(cube_pattern, self.area, portal_builder)

        self.moves = []
        for c in next(inp_iter):
            if c in ["L", "R"]:
                self.moves.append(c)
            else:
                if self.moves and type(self.moves[-1]) == int:
                    self.moves[-1] = self.moves[-1] * 10 + int(c)
                else:
                    self.moves.append(int(c))

        self.init_pos = (0, 0)
        self.init_direction = D.EAST

    def single_move(self, pos, d, move, handler):
        if type(move) == str:
            return pos, D_TURNS[d][move]

        while move > 0:
            next_pos, next_d = handler(pos, d)
            while self.area[next_pos] == 0:
                next_pos, next_d = handler(next_pos, next_d)
            if self.area[next_pos] == 1:
                break
            move -= 1
            pos = next_pos
            d = next_d

        return pos, d

    @staticmethod
    def _build_password(pos: tuple[int, int], direction: D) -> int:
        return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + SIDES.index(direction)

    def part_a(self):
        pos, d = self.init_pos, self.init_direction
        spacer = Spacer(*self.area.shape)
        for move in self.moves:
            pos, d = self.single_move(pos, d, move, lambda pp, dd: (spacer.move(pp, dd), dd))
        return self._build_password(pos, d)

    def part_b(self):
        pos, d = self.init_pos, self.init_direction
        for move in self.moves:
            pos, d = self.single_move(pos, d, move, lambda pp, dd: self.cube.move(pp, dd))
        return self._build_password(pos, d)


def test_simple():
    cube_pattern = [
        [0, 0, 1, 0],
        [5, 4, 2, 0],
        [0, 0, 6, 3],
    ]

    def _build_portals(data, dim, sides):
        portals = np.empty_like(data, dtype=object)
        for i in range(portals.shape[0]):
            for j in range(portals.shape[1]):
                portals[i, j] = {side: (t_sum((i, j), side), side) for side in SIDES}
        # 1 <-> 5
        for x in range(dim):
            s1_pos = t_sum(sides[1], (0, x))
            s5_pos = t_sum(sides[5], (0, dim - x - 1))
            portals[s1_pos][D.NORTH] = (s5_pos, D.SOUTH)
            portals[s5_pos][D.NORTH] = (s1_pos, D.SOUTH)
        # 1 <-> 4
        for x in range(dim):
            s1_pos = t_sum(sides[1], (x, 0))
            s4_pos = t_sum(sides[4], (0, x))
            portals[s1_pos][D.WEST] = (s4_pos, D.SOUTH)
            portals[s4_pos][D.NORTH] = (s1_pos, D.EAST)
        # 1 <-> 3
        for x in range(dim):
            s1_pos = t_sum(sides[1], (x, dim - 1))
            s3_pos = t_sum(sides[3], (x, dim - 1))
            portals[s1_pos][D.EAST] = (s3_pos, D.WEST)
            portals[s3_pos][D.EAST] = (s1_pos, D.WEST)
        # 2 <-> 3
        for x in range(dim):
            s2_pos = t_sum(sides[2], (x, dim - 1))
            s3_pos = t_sum(sides[3], (0, dim - x - 1))
            portals[s2_pos][D.EAST] = (s3_pos, D.SOUTH)
            portals[s3_pos][D.NORTH] = (s2_pos, D.WEST)
        # 4 <-> 6
        for x in range(dim):
            s4_pos = t_sum(sides[4], (dim - 1, x))
            s6_pos = t_sum(sides[6], (dim - x - 1, 0))
            portals[s4_pos][D.SOUTH] = (s6_pos, D.EAST)
            portals[s6_pos][D.WEST] = (s4_pos, D.NORTH)
        # 5 <-> 6
        for x in range(dim):
            s5_pos = t_sum(sides[5], (dim - 1, x))
            s6_pos = t_sum(sides[6], (dim - 1, dim - x - 1))
            portals[s5_pos][D.SOUTH] = (s6_pos, D.NORTH)
            portals[s6_pos][D.SOUTH] = (s5_pos, D.NORTH)
        # 5 <-> 3
        for x in range(dim):
            s5_pos = t_sum(sides[5], (x, 0))
            s3_pos = t_sum(sides[3], (dim - 1, dim - x - 1))
            portals[s5_pos][D.WEST] = (s3_pos, D.NORTH)
            portals[s3_pos][D.SOUTH] = (s5_pos, D.EAST)

        return portals

    solution = Solution(Input(0), cube_pattern, _build_portals)
    assert solution.part_a() == 6032
    assert solution.part_b() == 5031


def test_challenge():
    cube_pattern = [
        [0, 1, 3],
        [0, 2, 0],
        [4, 6, 0],
        [5, 0, 0],
    ]

    def _build_portals(data, dim, sides):
        portals = np.empty_like(data, dtype=object)
        for i in range(portals.shape[0]):
            for j in range(portals.shape[1]):
                portals[i, j] = {side: (t_sum((i, j), side), side) for side in SIDES}
        # 1 <-> 5
        for x in range(dim):
            s1_pos = t_sum(sides[1], (0, x))
            s5_pos = t_sum(sides[5], (x, 0))
            portals[s1_pos][D.NORTH] = (s5_pos, D.EAST)
            portals[s5_pos][D.WEST] = (s1_pos, D.SOUTH)
        # 1 <-> 4
        for x in range(dim):
            s1_pos = t_sum(sides[1], (x, 0))
            s4_pos = t_sum(sides[4], (dim - 1 - x, 0))
            portals[s1_pos][D.WEST] = (s4_pos, D.EAST)
            portals[s4_pos][D.WEST] = (s1_pos, D.EAST)
        # 2 <-> 4
        for x in range(dim):
            s2_pos = t_sum(sides[2], (x, 0))
            s4_pos = t_sum(sides[4], (0, x))
            portals[s2_pos][D.WEST] = (s4_pos, D.SOUTH)
            portals[s4_pos][D.NORTH] = (s2_pos, D.EAST)
        # 2 <-> 3
        for x in range(dim):
            s2_pos = t_sum(sides[2], (x, dim - 1))
            s3_pos = t_sum(sides[3], (dim - 1, x))
            portals[s2_pos][D.EAST] = (s3_pos, D.NORTH)
            portals[s3_pos][D.SOUTH] = (s2_pos, D.WEST)
        # 6 <-> 3
        for x in range(dim):
            s6_pos = t_sum(sides[6], (x, dim - 1))
            s3_pos = t_sum(sides[3], (dim - 1 - x, dim - 1))
            portals[s6_pos][D.EAST] = (s3_pos, D.WEST)
            portals[s3_pos][D.EAST] = (s6_pos, D.WEST)
        # 5 <-> 3
        for x in range(dim):
            s5_pos = t_sum(sides[5], (dim - 1, x))
            s3_pos = t_sum(sides[3], (0, x))
            portals[s5_pos][D.SOUTH] = (s3_pos, D.SOUTH)
            portals[s3_pos][D.NORTH] = (s5_pos, D.NORTH)
        # 5 <-> 6
        for x in range(dim):
            s5_pos = t_sum(sides[5], (x, dim - 1))
            s6_pos = t_sum(sides[6], (dim - 1, x))
            portals[s5_pos][D.EAST] = (s6_pos, D.NORTH)
            portals[s6_pos][D.SOUTH] = (s5_pos, D.WEST)

        return portals

    solution = Solution(Input(), cube_pattern, _build_portals)
    assert solution.part_a() == 26558
    assert solution.part_b() == 110400
