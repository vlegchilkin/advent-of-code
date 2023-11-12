import collections

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.space import Spacer, C_BORDERS
from solutions.python.aoc.tpl import t_dist, t_minmax


class Year2018Day6(Solution):
    """2018/6: Chronal Coordinates"""

    def __init__(self, inp: Input):
        self.points = inp.get_lines(lambda line: tuple(map(int, line.split(", "))))

    def part_a(self):
        step_limit = 100
        spacer = Spacer(ranges=None, directions=C_BORDERS)
        for _id, point in enumerate(self.points):
            spacer[complex(point[1], point[0])] = (_id, 0)

        q = collections.deque(spacer.at)
        infinite = set()
        while q:
            pos = q.popleft()
            _id, steps = spacer[pos]

            if steps > step_limit:
                infinite.add(_id)
                continue

            for _pos in spacer.links(
                pos, has_path=lambda p: (v := spacer.get(p)) is None or (v[0] != _id and v[1] == steps + 1)
            ):
                if _pos not in spacer:
                    spacer[_pos] = (_id, steps + 1)
                    q.append(_pos)
                else:
                    spacer[_pos] = (None, steps + 1)

        c = collections.Counter(v[0] for v in spacer.at.values() if v[0] is not None)
        best = max(v for k, v in c.items() if k is not None and k not in infinite)
        return best

    def part_b(self):
        def within(x, y, limit=10000):
            t = 0
            for p in self.points:
                t += t_dist((x, y), p)
                if t >= limit:
                    return False
            return True

        mm = t_minmax(self.points)
        return sum(within(x, y) for x in range(mm[0][0], mm[1][0]) for y in range(mm[0][1], mm[1][1]))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day6)
