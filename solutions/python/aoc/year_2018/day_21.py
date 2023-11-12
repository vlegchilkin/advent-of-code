import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.tpl import t_replace
from solutions.python.aoc.year_2018.day_19 import Year2018Day19


class Year2018Day21(Solution):
    """2018/21: Chronal Conversion"""

    def __init__(self, inp: Input):
        self.runner = Year2018Day19(inp)

    def part_a_b(self):
        """
          0..4:     ...
             5:     _5 = 0
            30:     while True:
             6:       _1 = _5 | 65536
             7:       _5 = 10678677
        13..16:       while _1:
         8..12:         _5 = (((_5 + (_1 & 255)) & 16777215) * 65899) & 16777215
        17..27:         _1 //= 256
            28:       if _5 == _0:
            29:         break

         the interceptor makes '_1//=256' faster and collects all possible hashes till the first repeat
        """
        possible = []

        def interceptor(index, regs):
            _index, _regs = index, regs
            if index == 28:
                if regs[5] in possible:
                    _index = None
                else:
                    possible.append(regs[5])
            elif index == 15:
                _regs = t_replace(regs, 1, regs[1] // 256)
                _index = 8
            return _index, _regs

        self.runner.execute((0, 0, 0, 0, 0, 0), interceptor)
        return possible[0], possible[-1]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day21)
