import copy
from enum import IntEnum

import pytest
import collections as cl
from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import Spacer, C, C_BORDERS
from aoc.year_2019 import IntcodeComputer

COMMANDS = {
    C.NORTH: 1,
    C.SOUTH: 2,
    C.WEST: 3,
    C.EAST: 4,
}


class TileType(IntEnum):
    WALL = 0
    EMPTY = 1
    OXY_GATE = 2


class Year2019Day15(Solution):
    """2019/15: Oxygen System"""

    def __init__(self, inp: Input):
        self.instructions = list(map(int, inp.get_text().split(",")))

    def part_a_b(self):
        spacer = Spacer(ranges=None)
        state = 0j, IntcodeComputer(self.instructions), 0
        queue = cl.deque([state])
        spacer[state[0]] = 1
        part_a, oxy_pos = None, None
        while queue:
            pos, computer, steps = queue.popleft()
            for direction, command in COMMANDS.items():
                if (n_pos := pos + direction) in spacer:
                    continue
                n_computer = copy.deepcopy(computer)
                tile_type = n_computer.run([command])[0]
                spacer[n_pos] = tile_type
                if tile_type == TileType.OXY_GATE:
                    part_a = steps + 1
                    oxy_pos = n_pos
                if tile_type != TileType.WALL:
                    queue.append((n_pos, n_computer, steps + 1))

        queue = cl.deque([(0, oxy_pos)])
        part_b = 0
        while queue:
            steps, pos = queue.popleft()
            part_b = max(part_b, steps)
            for n_pos in spacer.links(pos, C_BORDERS, has_path=lambda x: spacer[x] == 1):
                spacer[n_pos] = 2
                queue.append((steps + 1, n_pos))

        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day15)
