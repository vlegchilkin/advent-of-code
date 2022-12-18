from typing import Optional

from aoc_2022 import Input
import networkx as nx

D = [
    [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
    [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)],
    [(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)],
    [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)],
    [(1, 0, 0), (1, 0, 1), (1, 1, 1), (1, 1, 0)],
    [(0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1)],
]

T = [(0, 0, -1), (-1, 0, 0), (0, -1, 0), (0, 0, 1), (1, 0, 0), (0, 1, 0)]


class Solution:
    def __init__(self, inp: Input):
        self.cubes = [tuple([int(c) for c in line.split(",")]) for line in inp.get_lines()]

    def _get_alive(self):
        s_cubes = set(self.cubes)
        alive = []
        for i, a in enumerate(self.cubes):
            for j, d in enumerate(T):
                b = a[0] + d[0], a[1] + d[1], a[2] + d[2]
                if b not in s_cubes:
                    alive.append((i, j))
        return alive

    def _touch(self, x, y) -> Optional:
        c1, c2 = self.cubes[x[0]], self.cubes[y[0]]
        dx, dy, dz = abs(c1[0] - c2[0]), abs(c1[1] - c2[1]), abs(c1[2] - c2[2])
        if max(dx, dy, dz) > 1 or dx + dy + dz > 2:  # don't edge touch
            return

        t1, t2 = T[x[1]], T[y[1]]
        if t1[0] + t2[0] == 0 and t1[1] + t2[1] == 0 and t1[2] + t2[2] == 0:  # opposite sides
            return

        d1, d2 = D[x[1]], D[y[1]]

        p1 = set([(c1[0] + p[0], c1[1] + p[1], c1[2] + p[2]) for p in d1])
        p2 = set([(c2[0] + p[0], c2[1] + p[1], c2[2] + p[2]) for p in d2])
        common = p1.intersection(p2)
        if len(common) == 2:
            return tuple(sorted(common))

    def part_a(self):
        return len(self._get_alive())

    def part_b(self):
        a = self._get_alive()
        n = len(a)
        links = [dict() for _ in range(n)]
        for i in range(n - 1):
            li = links[i]
            for j in range(i + 1, n):
                if c := self._touch(a[i], a[j]):
                    lj = links[j]
                    if c not in li or ((prev := li[c]) and prev[0] == a[i][0]):
                        li[c] = a[j]
                    if c not in lj or ((prev := lj[c]) and prev[0] == a[j][0]):
                        lj[c] = a[i]

        graph = nx.Graph()
        for i, l in enumerate(links):
            for c in l.values():
                graph.add_edge(a[i], c)

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
