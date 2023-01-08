from typing import Iterator

import numpy as np

from aoc import Input, PuzzleData, ISolution
from aoc.space import C, Spacer, ItFunc, C_OPPOSITE, C_TURNS, IT

SIDES = [C.EAST, C.SOUTH, C.WEST, C.NORTH]


class Cube:
    def __init__(self, pattern, data: Spacer, links):
        self.offsets = {}
        self.dim = data.n // len(pattern)
        for off_i, v in enumerate(pattern):
            for off_j, side in enumerate(v):
                if not side:
                    continue
                self.offsets[side] = complex(self.dim * off_i, self.dim * off_j)
        self.portals = self._build_portals(data.shape, links)

    def _build_portals(self, shape, links) -> Spacer:
        portals = Spacer(shape)
        for pos in portals.iter():
            portals[pos] = {side: (pos + side, side) for side in SIDES}

        s = Spacer((self.dim, self.dim))

        def make_link(side_a, dir_a, it_a: ItFunc, side_b, dir_b, it_b: ItFunc):
            for x, y in zip(s.iter(it=it_a), s.iter(it=it_b)):
                sa_pos = self.offsets[side_a] + x
                sb_pos = self.offsets[side_b] + y
                portals[sa_pos][dir_a] = (sb_pos, C_OPPOSITE[dir_b])
                portals[sb_pos][dir_b] = (sa_pos, C_OPPOSITE[dir_a])

        for link in links:
            make_link(*link)

        return portals

    def move(self, pos: complex, direction: C) -> (complex, C):
        return self.portals[pos][direction]


class Solution(ISolution):
    def __init__(self, inp: Input, cube_pattern: list[list], links):
        inp_iter = inp.get_iter()
        self.area = self._build_area(inp_iter)
        self.cube = Cube(cube_pattern, self.area, links)
        self.moves = self._build_moves(inp_iter)
        self.init_pos = 0
        self.init_direction = C.EAST

    @staticmethod
    def _build_area(inp_iter: Iterator[str]):
        area_data = []
        while line := next(inp_iter):
            area_data.append(list(line))

        shape = len(area_data), max([len(r) for r in area_data])
        area = np.zeros(shape, dtype=int)
        cross = {".": -1, "#": 1, " ": 0}
        for i, row in enumerate(area_data):
            for j, c in enumerate(row):
                area[i, j] = cross[c]
        return Spacer.build(area)

    @staticmethod
    def _build_moves(inp_iter: Iterator[str]):
        moves = []
        for c in next(inp_iter):
            if c in ["L", "R"]:
                moves.append(c)
            else:
                if moves and type(moves[-1]) == int:
                    moves[-1] = moves[-1] * 10 + int(c)
                else:
                    moves.append(int(c))
        return moves

    def single_move(self, pos, d, move, handler):
        if type(move) == str:
            return pos, C_TURNS[d][move]

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
    def _build_password(pos: complex, direction: C) -> int:
        return 1000 * (int(pos.real) + 1) + 4 * (int(pos.imag) + 1) + SIDES.index(direction)

    def part_a(self):
        pos, d = self.init_pos, self.init_direction
        for move in self.moves:
            pos, d = self.single_move(pos, d, move, lambda pp, dd: (self.area.move(pp, dd), dd))
        return self._build_password(pos, d)

    def part_b(self):
        pos, d = self.init_pos, self.init_direction
        for move in self.moves:
            pos, d = self.single_move(pos, d, move, lambda pp, dd: self.cube.move(pp, dd))
        return self._build_password(pos, d)


def test_simple():
    pd = PuzzleData("0")
    cube_pattern = [
        [0, 0, 1, 0],
        [5, 4, 2, 0],
        [0, 0, 6, 3],
    ]

    links = [
        (1, C.NORTH, IT.TOP_LR, 5, C.NORTH, IT.TOP_RL),
        (1, C.WEST, IT.LEFT_TB, 4, C.NORTH, IT.TOP_LR),
        (1, C.EAST, IT.RIGHT_TB, 3, C.EAST, IT.RIGHT_TB),
        (2, C.EAST, IT.RIGHT_TB, 3, C.NORTH, IT.TOP_RL),
        (4, C.SOUTH, IT.BOTTOM_LR, 6, C.WEST, IT.LEFT_BT),
        (5, C.SOUTH, IT.BOTTOM_LR, 6, C.SOUTH, IT.BOTTOM_RL),
        (5, C.WEST, IT.LEFT_TB, 3, C.SOUTH, IT.BOTTOM_RL),
    ]

    solution = Solution(pd.inp, cube_pattern, links)
    assert solution.part_a() == int(pd.out.a)
    assert solution.part_b() == int(pd.out.b)


def test_challenge():
    pd = PuzzleData("puzzle")
    cube_pattern = [
        [0, 1, 3],
        [0, 2, 0],
        [4, 6, 0],
        [5, 0, 0],
    ]

    links = [
        (1, C.NORTH, IT.TOP_LR, 5, C.WEST, IT.LEFT_TB),
        (1, C.WEST, IT.LEFT_TB, 4, C.WEST, IT.LEFT_BT),
        (2, C.WEST, IT.LEFT_TB, 4, C.NORTH, IT.TOP_LR),
        (2, C.EAST, IT.RIGHT_TB, 3, C.SOUTH, IT.BOTTOM_LR),
        (6, C.EAST, IT.RIGHT_TB, 3, C.EAST, IT.RIGHT_BT),
        (5, C.SOUTH, IT.BOTTOM_LR, 3, C.NORTH, IT.TOP_LR),
        (5, C.EAST, IT.RIGHT_TB, 6, C.SOUTH, IT.BOTTOM_LR),
    ]

    solution = Solution(Input(), cube_pattern, links)
    assert solution.part_a() == int(pd.out.a)
    assert solution.part_b() == int(pd.out.b)
