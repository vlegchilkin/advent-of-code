from collections import deque

import pytest

from aoc import Input, Spacer, D_BORDERS, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        arr = inp.get_array()
        self.spacer = Spacer(*arr.shape, default_directions=D_BORDERS)

        self.a = self.spacer.new_array(0)
        self.start = self.finish = None
        for x in self.spacer.iter():
            ch = arr[x]
            if ch == "S":
                self.start = x
                ch = "a"
            elif ch == "E":
                self.finish = x
                ch = "z"
            self.a[x] = ord(ch) - ord("a")

        self.paths = self._build_paths()

    def _build_paths(self):
        visited = self.spacer.new_array(-1)
        visited[self.finish] = 0

        queue = deque([self.finish])
        while queue:
            from_pos = queue.popleft()
            for to_pos in self.spacer.get_links(from_pos):
                if visited[to_pos] == -1 and self.a[from_pos] <= self.a[to_pos] + 1:
                    visited[to_pos] = visited[from_pos] + 1
                    queue.append(to_pos)
        return visited

    def part_a(self):
        return self.paths[self.start]

    def part_b(self):
        return min([self.paths[x] for x in self.spacer.iter(lambda pos: self.paths[pos] != -1 and self.a[pos] == 0)])


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
