import queue
import re
from functools import cache

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.tpl import t_sum


class Year2018Day22(Solution):
    """2018/22: Mode Maze"""

    def __init__(self, inp: Input):
        lines = inp.get_lines(lambda line: tuple(map(int, re.findall(r"\d+", line))))
        self.depth = lines[0][0]
        self.target = lines[1]

    def part_a_b(self):
        @cache
        def geo_index(x, y):
            if (x, y) in [(0, 0), self.target]:
                return 0
            if y == 0:
                return x * 16807
            elif x == 0:
                return y * 48271
            return ero_level(x - 1, y) * ero_level(x, y - 1)

        @cache
        def ero_level(x, y):
            return (geo_index(x, y) + self.depth) % 20183

        @cache
        def get_type(x, y):
            if x < 0 or y < 0:
                return None
            return ero_level(x, y) % 3

        part_a = sum(get_type(x, y) for x in range(self.target[0] + 1) for y in range(self.target[1] + 1))

        # rocky=0, wet=1, narrow=1
        # torch=0, climbing gear=1, neither=2
        type_tools = {0: [0, 1], 1: [1, 2], 2: [0, 2]}
        finish_state = (self.target, 0)
        shortest = {((0, 0), 0): 0, ((0, 0), 1): 7}
        q = queue.PriorityQueue()
        for state, path in shortest.items():
            q.put((path, state))

        part_b = None
        while not q.empty():
            path, (pos, tool) = q.get()
            if (pos, tool) == finish_state:
                part_b = path
                break
            if shortest[(pos, tool)] < path:
                continue
            for d in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                _pos = t_sum(pos, d)
                if (_type := get_type(*_pos)) is None or tool not in (allowed_tools := type_tools[_type]):
                    continue
                for _tool in allowed_tools:
                    _path = path + 1 + (7 if tool != _tool else 0)
                    if (_pos, _tool) not in shortest or shortest[(_pos, _tool)] > _path:
                        shortest[(_pos, _tool)] = _path
                        q.put((_path, (_pos, _tool)))
        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day22)
