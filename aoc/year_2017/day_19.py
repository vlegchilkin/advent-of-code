import string

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution
from aoc.space import Spacer, C_BORDERS, C, C_TURNS


class Year2017Day19(ISolution):
    """2017/19: A Series of Tubes"""

    def __init__(self, inp: Input):
        self.data = inp.get_array(lambda s: s if s != " " else None)

    def part_a_b(self):
        spacer = Spacer.build(self.data, directions=C_BORDERS)
        pos, direction = next(pos for pos, v in spacer if v == "|"), C.SOUTH
        response, steps = [], 1
        while c := spacer.get(pos := spacer.move(pos, direction)):
            steps += 1
            if c in string.ascii_uppercase:
                response.append(c)
            elif c == "+":
                if (pos + (d := C_TURNS[direction]["R"])) in spacer:
                    direction = d
                else:
                    direction = C_TURNS[direction]["L"]

        return "".join(response), steps


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day19)
