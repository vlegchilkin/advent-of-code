import pytest

from enum import StrEnum
from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
import collections as cl


class SpaceObject(StrEnum):
    CENTER_OF_MASS = "COM"
    SANTA = "SAN"
    YOU = "YOU"


class Year2019Day6(Solution):
    """2019/6: Universal Orbit Map"""

    def __init__(self, inp: Input):
        self.orbits = inp.get_lines(lambda x: x.split(")"))

    def part_a(self):
        tree = cl.defaultdict(list)
        for k, v in self.orbits:
            tree[k].append(v)

        def dfs(node, depth):
            total = depth
            for child in tree[node]:
                total += dfs(child, depth + 1)
            return total

        return dfs(SpaceObject.CENTER_OF_MASS, 0)

    def part_b(self):
        parent = {}
        for k, v in self.orbits:
            parent[v] = k

        def fill_path(path, node):
            path.append(node)
            return fill_path(path, parent[node]) if node != SpaceObject.CENTER_OF_MASS else path

        santa_path = fill_path([], SpaceObject.SANTA)
        your_path = fill_path([], SpaceObject.YOU)
        index = -1
        while santa_path[index] == your_path[index]:
            index -= 1

        return len(your_path) + len(santa_path) + 2 * index


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day6)
