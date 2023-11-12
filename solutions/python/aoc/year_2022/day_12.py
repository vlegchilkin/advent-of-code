from collections import deque

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import Spacer, C_BORDERS


class Year2022Day12(Solution):
    def __init__(self, inp: Input):
        arr = inp.get_array(decoder=lambda c: ord(c) - ord("a"))
        self.spacer = Spacer.build(arr, directions=C_BORDERS)

        self.start = self.finish = None
        for pos, v in self.spacer:
            if v == -14:
                self.start = pos
                self.spacer.at[pos] = 0
            elif v == -28:
                self.finish = pos
                self.spacer.at[pos] = 25

        self.paths = self._build_paths()

    def _build_paths(self):
        visited = {self.finish: 0}
        queue = deque([self.finish])
        while queue:
            from_pos = queue.popleft()
            for to_pos in self.spacer.links(from_pos):
                if to_pos not in visited and self.spacer.at[from_pos] <= self.spacer.at[to_pos] + 1:
                    visited[to_pos] = visited[from_pos] + 1
                    queue.append(to_pos)
        return visited

    def part_a(self):
        return self.paths[self.start]

    def part_b(self):
        return min([self.paths[p] for p, v in self.spacer if v == 0 and p in self.paths])


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2022Day12)
