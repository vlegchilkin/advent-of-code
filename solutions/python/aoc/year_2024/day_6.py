import copy

import pytest
import collections as cl

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import Spacer, C_MOVES, C_TURNS


class LoopDetected(Exception):
    pass


class Year2024Day6(Solution):
    """2024/6: Guard Gallivant"""

    def __init__(self, inp: Input):
        self.space = Spacer.build(inp.get_array())

    @staticmethod
    def _run(space, s_pos, s_direction):
        visited = cl.defaultdict(set)
        pos, direction = s_pos, s_direction
        while pos in space:
            dirs = visited[pos]
            if direction in dirs:
                raise LoopDetected()

            dirs.add(direction)

            n_pos = pos + direction
            if space.get(n_pos) == "#":
                direction = C_TURNS[direction]["R"]
            else:
                pos = n_pos

        return len(visited)

    def part_a(self):
        pos, direction = next((p, C_MOVES[v]) for p, v in self.space if v in C_MOVES)
        return self._run(self.space, pos, direction)

    def part_b(self):
        pos, direction = next((p, C_MOVES[v]) for p, v in self.space if v in C_MOVES)
        possible = [pos for pos, v in self.space if v != "#"]
        space = copy.deepcopy(self.space)
        loops = 0
        for obs_pos in possible:
            space[obs_pos] = "#"
            try:
                self._run(space, pos, direction)
            except LoopDetected:
                loops += 1
            space[obs_pos] = self.space[obs_pos]
        return loops

@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2024Day6)
