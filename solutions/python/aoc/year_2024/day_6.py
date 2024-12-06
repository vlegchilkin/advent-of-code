import copy

import pytest
import collections as cl

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import Spacer, C_MOVES, C_TURNS, C


class LoopDetected(Exception):
    pass


class Year2024Day6(Solution):
    """2024/6: Guard Gallivant"""

    def __init__(self, inp: Input):
        self.space = Spacer.build(inp.get_array())

    @staticmethod
    def _run(space, s_pos, s_direction) -> dict[complex, set[C]]:
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

        return visited

    def part_a_b(self):
        start_pos, start_direction = next((p, C_MOVES[v]) for p, v in self.space if v in C_MOVES)
        visited_pos_directions = self._run(self.space, start_pos, start_direction)

        space = copy.deepcopy(self.space)
        loops = 0
        for obstacle_pos in visited_pos_directions.keys():
            space[obstacle_pos] = "#"
            try:
                self._run(space, start_pos, start_direction)
            except LoopDetected:
                loops += 1
            space[obstacle_pos] = self.space[obstacle_pos]

        part_a = len(visited_pos_directions)
        part_b = loops
        return part_a, part_b

@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2024Day6)
