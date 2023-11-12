import itertools

import pytest
import numpy as np
from numpy import Inf

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.space import Spacer, C_BORDERS


class Year2016Day24(Solution):
    """2016/24: Air Duct Spelunking"""

    def __init__(self, inp: Input):
        self.maze = inp.get_array(decoder=lambda v: v if v in ".0123456789" else None)

    def part_a_b(self):
        nums = {v: complex(*pos) for pos, v in np.ndenumerate(self.maze) if v and v != "."}
        d = {}
        spacer = Spacer.build(self.maze, directions=C_BORDERS)
        for num, start_pos in nums.items():
            paths, _ = spacer.bfs(start_pos)
            for _num, end_pos in nums.items():
                d[(num, _num)] = paths[end_pos][0]

        part_a = part_b = Inf
        for c in itertools.permutations(set(nums) - {"0"}):
            part_a = min(part_a, d[("0", c[0])] + sum([d[p] for p in itertools.pairwise(c)]))
            part_b = min(part_b, d[("0", c[0])] + sum([d[p] for p in itertools.pairwise(c)]) + d[(c[-1], "0")])
        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day24)
