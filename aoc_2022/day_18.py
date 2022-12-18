from itertools import combinations
from typing import Optional

from aoc_2022 import Input
import networkx as nx

SIDE_VERTEXES = {
    (0, 0, -1): [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
    (-1, 0, 0): [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)],
    (0, -1, 0): [(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)],
    (0, 0, 1): [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)],
    (1, 0, 0): [(1, 0, 0), (1, 0, 1), (1, 1, 1), (1, 1, 0)],
    (0, 1, 0): [(0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1)],
}


class Solution:
    def __init__(self, inp: Input):
        self.cubes = set([tuple([int(c) for c in line.split(",")]) for line in inp.get_lines()])

    def _get_alive(self):
        alive = []
        for cube in self.cubes:
            for t in SIDE_VERTEXES:
                if tuple(map(sum, zip(cube, t))) not in self.cubes:
                    alive.append((cube, t))
        return alive

    @staticmethod
    def _get_sides_link(a, b) -> Optional:
        cube_a, side_a = a
        cube_b, side_b = b

        dx, dy, dz = abs(cube_a[0] - cube_b[0]), abs(cube_a[1] - cube_b[1]), abs(cube_a[2] - cube_b[2])
        if max(dx, dy, dz) > 1 or dx + dy + dz > 2:
            return  # cubes a & b too far away to have a common edge

        if side_a[0] + side_b[0] == side_a[1] + side_b[1] == side_a[2] + side_b[2] == 0:
            return  # opposite sides of cubes can't be linked

        p1 = set([tuple(map(sum, zip(cube_a, p))) for p in SIDE_VERTEXES[side_a]])
        p2 = set([tuple(map(sum, zip(cube_b, p))) for p in SIDE_VERTEXES[side_b]])
        if len(common := p1 & p2) == 2:
            return tuple(sorted(common))  # cubes touched within an edge by 2 common points

    def part_a(self):
        return len(self._get_alive())

    def part_b(self):
        alive = self._get_alive()
        links = dict()
        for a, b in combinations(alive, 2):
            if c := self._get_sides_link(a, b):
                la = links.setdefault(a, {})
                if c not in la or ((prev := la[c]) and prev[0] == a[0]):  # same cube has low priority in links for edge
                    la[c] = b
                lb = links.setdefault(b, {})
                if c not in lb or ((prev := lb[c]) and prev[0] == b[0]):  # same cube has low priority in links for edge
                    lb[c] = a

        graph = nx.Graph()
        for f, l in links.items():
            for c in l.values():
                graph.add_edge(f, c)

        components = list(nx.connected_components(graph))

        return max([len(c) for c in components])


def test_simple():
    solution = Solution(Input(0))
    assert solution.part_a() == 64
    assert solution.part_b() == 58


def test_ideal():
    solution = Solution(Input("ideal"))
    assert solution.part_a() == 36
    assert solution.part_b() == 30


def test_challenge():
    solution = Solution(Input())
    assert solution.part_a() == 4364
    assert solution.part_b() == 2508
