from collections import deque
from itertools import combinations
from typing import Optional

import networkx as nx
import pytest

from aoc import Input, t_sum, t_delta, t_minmax, t_inside, get_puzzles, PuzzleData

# 6 cube sides with 4 vertexes of each side
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

    def _get_clean_sides(self):
        clean = []
        for cube in self.cubes:
            for t in SIDE_VERTEXES:
                if tuple(map(sum, zip(cube, t))) not in self.cubes:
                    clean.append((cube, t))
        return clean

    @staticmethod
    def _get_sides_common_edge(a, b) -> Optional:
        cube_a, side_a = a
        cube_b, side_b = b

        if sum(d := t_delta(cube_a, cube_b)) > 2 or max(d) > 1:
            return  # cubes a & b too far away to have a common edge

        if side_a[0] + side_b[0] == side_a[1] + side_b[1] == side_a[2] + side_b[2] == 0:
            return  # opposite sides of cubes can't be linked

        vertexes_a = set([t_sum(cube_a, p) for p in SIDE_VERTEXES[side_a]])
        vertexes_b = set([t_sum(cube_b, p) for p in SIDE_VERTEXES[side_b]])
        if len(common := vertexes_a & vertexes_b) == 2:
            return tuple(sorted(common))  # cubes touched within an edge in 2 common points

    def part_a(self):
        return len(self._get_clean_sides())

    def part_b_graphs(self):
        clean_sides = self._get_clean_sides()
        side_edges = dict()
        for a, b in combinations(clean_sides, 2):
            if edge := self._get_sides_common_edge(a, b):
                # sides from the same cube has low priority in links for each edge
                la = side_edges.setdefault(a, {})
                if not (existent := la.get(edge)) or existent[0] == a[0]:
                    la[edge] = b
                lb = side_edges.setdefault(b, {})
                if not (existent := lb.get(edge)) or existent[0] == b[0]:
                    lb[edge] = a

        graph = nx.Graph()
        for side_a, edges in side_edges.items():
            for side_b in edges.values():
                graph.add_edge(side_a, side_b)

        connected_components = list(nx.connected_components(graph))

        return max([len(c) for c in connected_components])

    def part_b_bfs(self):
        mm = t_minmax(self.cubes)
        limits = t_sum(mm[0], (-1, -1, -1)), t_sum(mm[1], (1, 1, 1))
        queue, visible, source = deque(), 0, limits[0]
        visited = {source}
        queue.append(source)

        while queue:
            pos = queue.popleft()
            for side in SIDE_VERTEXES:
                next_pos = t_sum(pos, side)
                if t_inside(next_pos, limits) and next_pos not in visited:
                    if next_pos in self.cubes:
                        visible += 1
                    else:
                        visited.add(next_pos)
                        queue.append(next_pos)
        return visible

    def part_b(self):
        assert (result := self.part_b_bfs()) == self.part_b_graphs()
        return result


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
