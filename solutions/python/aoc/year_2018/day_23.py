import re
from itertools import pairwise, product

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.tpl import t_dist


class Year2018Day23(Solution):
    """2018/23: Experimental Emergency Teleportation"""

    def __init__(self, inp: Input):
        r = re.compile(r"^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)$")

        def parse(line):
            d = tuple(map(int, r.match(line).groups()))
            return d[3], d[:3]

        self.nanobots = inp.get_lines(parse)

    def part_a(self):
        radius, zero = max(self.nanobots)
        count = 0
        for _, pos in self.nanobots:
            if t_dist(zero, pos) <= radius:
                count += 1
        return count

    def part_b(self):
        """Bruteforce visible count from len(self.nanobots) down to 1 checking if it is possible via octree division"""
        space = tuple(
            (min(p[i] - r for r, p in self.nanobots), max(p[i] + r + 1 for r, p in self.nanobots)) for i in range(3)
        )

        def distance(ranges, point) -> int:
            """minimal manhattan distance from a point to a rectangle specified"""
            result = 0
            for i in range(3):
                if not (ranges[i][0] <= point[i] < ranges[i][1]):
                    result += min(abs(point[i] - ranges[i][0]), abs(point[i] - (ranges[i][1] - 1)))
            return result

        def bots_in_scan_range(ranges) -> int:
            """How many nanobots could scan at least single point in the rectangle specified"""
            return sum(distance(ranges, point) <= r for r, point in self.nanobots)

        def octree(ranges, limit, best):
            # split ranges space to 2^3=8 subspaces (each dimension by half)
            coord_steps = [(b, (b + e) // 2, e) for b, e in ranges]
            for x, y, z in product(*(pairwise(step) for step in coord_steps)):
                if x[0] == x[1] or y[0] == y[1] or z[0] == z[1]:
                    continue  # an empty rectangle

                if best is not None and distance((x, y, z), (0, 0, 0)) >= best:
                    continue  # already have better results than any from the region

                if bots_in_scan_range((x, y, z)) >= limit:  # best point might be in this subspace
                    if (x[1] - x[0]) + (y[1] - y[0]) + (z[1] - z[0]) == 3:
                        d = abs(x[0]) + abs(y[0]) + abs(z[0])  # atomic point in space, count distance to (0, 0, 0)
                    else:
                        d = octree((x, y, z), limit, best)
                    if best is None or (d is not None and d < best):
                        best = d

            return best

        for visible in range(len(self.nanobots), -1, -1):
            if (closest := octree(space, visible, None)) is not None:
                return closest


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day23)
