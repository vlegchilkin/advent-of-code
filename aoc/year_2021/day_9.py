import math

import pytest

from aoc import Input, get_puzzles, PuzzleData
from aoc.space import Spacer, C_BORDERS


class Solution:
    def __init__(self, inp: Input):
        self.a = inp.get_array(int)

    def part_a(self):
        spacer = Spacer.build(self.a, directions=C_BORDERS)
        result = 0
        for pos, value in spacer:
            if next(spacer.links(pos, test=lambda link: spacer.at[pos] >= spacer.at[link]), None) is None:
                result += value + 1
        return result

    def part_b(self):
        spacer = Spacer.build(self.a, directions=C_BORDERS)
        sizes, visited = [], set()
        for pos, value in spacer:
            if value != 9 and pos not in visited:
                paths, _ = spacer.bfs(pos, has_path=lambda link: spacer.at[link] != 9)
                visited |= paths.keys()
                sizes.append(len(paths))
        return math.prod(sorted(sizes, reverse=True)[:3])


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
