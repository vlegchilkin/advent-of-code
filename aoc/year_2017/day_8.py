import collections
import operator
import re

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Year2017Day8(ISolution):
    """2017/8: I Heard You Like Registers"""

    def __init__(self, inp: Input):
        r = re.compile(r"^(\w+) (inc|dec) (-?\d+) if (\w+) ([<>=!]+) (-?\d+)$")
        self.lines = inp.get_lines(lambda line: r.match(line).groups())

    def part_a_b(self):
        regs = collections.defaultdict(int)
        operators = {
            "<": operator.lt,
            ">": operator.gt,
            ">=": operator.ge,
            "<=": operator.le,
            "!=": operator.ne,
            "==": operator.eq,
        }
        commands = {
            "inc": operator.iadd,
            "dec": operator.isub,
        }

        absolute_max = 0
        for reg, cmd, value, if_reg, if_op, if_arg in self.lines:
            if operators[if_op](regs[if_reg], int(if_arg)):
                regs[reg] = commands[cmd](regs[reg], int(value))
                absolute_max = max(absolute_max, regs[reg])

        return max(regs.values()), absolute_max


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day8)
