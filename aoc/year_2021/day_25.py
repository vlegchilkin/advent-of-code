import itertools

import pytest

from aoc import Input, get_puzzles, PuzzleData
from aoc.space import Spacer, C


class Solution:
    def __init__(self, inp: Input):
        self.ar = inp.get_array(decoder=lambda x: {">": 1, "v": 2, ".": None}.get(x))

    def part_a(self):
        spacer = Spacer.build(self.ar)

        def do_step(sp):
            res = {}
            for pos, v in sp.items():
                if v == 1:
                    if (next_pos := spacer.move(pos, C.EAST)) not in sp:
                        res[next_pos] = v
                    else:
                        res[pos] = v
            for pos, v in sp.items():
                if v == 2:
                    if (next_pos := spacer.move(pos, C.SOUTH)) not in res and sp.get(next_pos) != 2:
                        res[next_pos] = v
                    else:
                        res[pos] = v
            return res

        space = spacer.at
        counter = itertools.count(1)
        while (_space := do_step(space)) != space:
            next(counter)
            space = _space
        return next(counter)

    def part_b(self):
        return ""


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
