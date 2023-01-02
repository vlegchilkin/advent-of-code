import itertools

import pytest

from aoc import Input, get_puzzles, PuzzleData
from aoc.space import Spacer


class Solution:
    def __init__(self, inp: Input):
        self.ar = inp.get_array(int)

    @staticmethod
    def flash(spacer):
        for p, v in spacer:
            spacer.at[p] = v + 1

        count = 0
        while count < 100:
            for p, v in spacer:
                if v > 9:
                    spacer.at[p] = 0
                    for link in spacer.links(p, has_path=lambda x: spacer.at[x] > 0):
                        spacer.at[link] += 1
                    count += 1
                    break
            else:
                break
        return count

    def part_a(self):
        spacer = Spacer.build(self.ar)
        return sum(self.flash(spacer) for _ in range(100))

    def part_b(self):
        spacer = Spacer.build(self.ar)
        return next(itertools.dropwhile(lambda _: self.flash(spacer) < 100, itertools.count(1)))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
