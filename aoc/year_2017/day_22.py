import math
from enum import IntEnum

import numpy as np

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution
from aoc.space import Spacer, C, C_TURNS
from aoc.tpl import t_koef


class State(IntEnum):
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3


class Year2017Day22(ISolution):
    """2017/22: Sporifica Virus"""

    def __init__(self, inp: Input):
        self.grid = inp.get_array(lambda s: s == "#" or None)
        self.start_pos = tuple(map(math.floor, t_koef(0.5, self.grid.shape)))
        self.start_direction = C.NORTH

    def part_a(self):
        infected = Spacer.build(self.grid, ranges=None)
        infect_bursts, pos, direction = 0, complex(*self.start_pos), self.start_direction
        for _ in range(10_000):
            if pos in infected:
                direction = C_TURNS[direction]["R"]
                del infected[pos]
            else:
                direction = C_TURNS[direction]["L"]
                infected[pos] = True
                infect_bursts += 1
            pos = pos + direction
        return infect_bursts

    def part_b(self):
        states = Spacer(ranges=None, at={complex(*pos): State.INFECTED for pos, v in np.ndenumerate(self.grid) if v})

        def move(st, d):
            if not st:
                return C_TURNS[d]["L"]
            elif st == State.WEAKENED:
                return d
            elif st == State.INFECTED:
                return C_TURNS[d]["R"]
            elif st == State.FLAGGED:
                return -d

        infect_bursts, pos, direction = 0, complex(*self.start_pos), self.start_direction
        for _ in range(10_000_000):
            state = states.get(pos)
            direction = move(state, direction)
            state = ((state or 0) + 1) % 4
            if state:
                states[pos] = state
                if state == State.INFECTED:
                    infect_bursts += 1
            else:
                del states[pos]
            pos = pos + direction
        return infect_bursts


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day22)
