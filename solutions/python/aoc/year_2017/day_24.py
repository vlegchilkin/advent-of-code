import operator
from functools import cache

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2017Day24(Solution):
    """2017/24: Electromagnetic Moat"""

    def __init__(self, inp: Input):
        self.chains = inp.get_lines(lambda line: tuple(map(int, line.split("/"))))

    def part_a_b(self):
        @cache
        def recu(last, used, total, func):
            best = total
            for i, (left, right) in enumerate(self.chains):
                if (left == last or right == last) and not ((1 << i) & used):
                    _last = right if left == last else left
                    _used = used + (1 << i)
                    _total = func(total, left + right)
                    best = max(best, recu(_last, _used, _total, func))
            return best

        part_a = recu(0, 0, 0, operator.add)
        part_b = recu(0, 0, (0, 0), lambda t, s: (t[0] + 1, t[1] + s))[1]
        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day24)
