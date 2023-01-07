from typing import Iterator

import numpy as np

from aoc import Input, D, Spacer, D_TURNS, D_OPPOSITE, IT, ItFunc, PuzzleData
from aoc.tpl import t_sum

SIDES = [D.EAST, D.SOUTH, D.WEST, D.NORTH]


class Cube:
    def __init__(self, pattern, data, links):
        self.offsets = {}
        self.dim = len(data) // len(pattern)
        for off_i, v in enumerate(pattern):
            for off_j, side in enumerate(v):
                if not side:
                    continue
                self.offsets[side] = (self.dim * off_i, self.dim * off_j)
        self.portals = self._build_portals(data.shape, links)

    def _build_portals(self, shape, links):
        portals = np.empty(shape, dtype=object)
        for i in range(portals.shape[0]):
            for j in range(portals.shape[1]):
                portals[i, j] = {side: (t_sum((i, j), side), side) for side in SIDES}

        s = Spacer(self.dim, self.dim)

        def make_link(side_a, dir_a, it_a: ItFunc, side_b, dir_b, it_b: ItFunc):
            for x, y in zip(s.iter(it=it_a), s.iter(it=it_b)):
                sa_pos = t_sum(self.offsets[side_a], x)
                sb_pos = t_sum(self.offsets[side_b], y)
                portals[sa_pos][dir_a] = (sb_pos, D_OPPOSITE[dir_b])
                portals[sb_pos][dir_b] = (sa_pos, D_OPPOSITE[dir_a])

        for link in links:
            make_link(*link)

        return portals

    def move(self, pos: tuple[int, int], direction: D) -> (tuple[int, int], D):
        return self.portals[pos][direction]


class Solution:
    def __init__(self, inp: Input, cube_pattern: list[list], links):
        inp_iter = inp.get_iter()
        self.area = self._build_area(inp_iter)
        self.cube = Cube(cube_pattern, self.area, links)
        self.moves = self._build_moves(inp_iter)
        self.init_pos = (0, 0)
        self.init_direction = D.EAST

    @staticmethod
    def _build_area(inp_iter: Iterator[str]):
        area_data = []
        while line := next(inp_iter):
            area_data.append(list(line))

        shape = len(area_data), max([len(r) for r in area_data])
        area = np.full(shape, dtype=int, fill_value=0)
        cross = {".": -1, "#": 1, " ": 0}
        for i, row in enumerate(area_data):
            for j, c in enumerate(row):
                area[i, j] = cross[c]
        return area

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
    pd = PuzzleData("0")
    cube_pattern = [
        [0, 0, 1, 0],
        [5, 4, 2, 0],
        [0, 0, 6, 3],
    ]

    links = [
        (1, D.NORTH, IT.TOP_LR, 5, D.NORTH, IT.TOP_RL),
        (1, D.WEST, IT.LEFT_TB, 4, D.NORTH, IT.TOP_LR),
        (1, D.EAST, IT.RIGHT_TB, 3, D.EAST, IT.RIGHT_TB),
        (2, D.EAST, IT.RIGHT_TB, 3, D.NORTH, IT.TOP_RL),
        (4, D.SOUTH, IT.BOTTOM_LR, 6, D.WEST, IT.LEFT_BT),
        (5, D.SOUTH, IT.BOTTOM_LR, 6, D.SOUTH, IT.BOTTOM_RL),
        (5, D.WEST, IT.LEFT_TB, 3, D.SOUTH, IT.BOTTOM_RL),
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
        (1, D.NORTH, IT.TOP_LR, 5, D.WEST, IT.LEFT_TB),
        (1, D.WEST, IT.LEFT_TB, 4, D.WEST, IT.LEFT_BT),
        (2, D.WEST, IT.LEFT_TB, 4, D.NORTH, IT.TOP_LR),
        (2, D.EAST, IT.RIGHT_TB, 3, D.SOUTH, IT.BOTTOM_LR),
        (6, D.EAST, IT.RIGHT_TB, 3, D.EAST, IT.RIGHT_BT),
        (5, D.SOUTH, IT.BOTTOM_LR, 3, D.NORTH, IT.TOP_LR),
        (5, D.EAST, IT.RIGHT_TB, 6, D.SOUTH, IT.BOTTOM_LR),
    ]

    solution = Solution(Input(), cube_pattern, links)
    assert solution.part_a() == int(pd.out.a)
    assert solution.part_b() == int(pd.out.b)
