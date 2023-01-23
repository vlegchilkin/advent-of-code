import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.math import factors
from aoc.tpl import t_add_pos
from aoc.year_2018.day_16 import execute


class Year2018Day19(Solution):
    """2018/19: Go With The Flow"""

    def __init__(self, inp: Input):
        it = inp.get_iter()
        self.ip = int(next(it).split(" ")[-1])
        self.instructions = [(r[0], *map(int, r[1:])) for r in map(lambda line: line.split(" "), it)]

    def run(self, regs):
        """
        1..16 steps are just an algorithm for a sum of factors of the register [2] with halt on a line 16:

        for [4] in 1..[2]:
          for [5] in 1..[2]:
            if [4]*[5] == [2]:
              [0] += [4]
        """
        while True:
            index = regs[self.ip]
            if index == 1:
                regs = t_add_pos(regs, 0, sum(factors(regs[2])))
                break
            regs = execute(regs, *self.instructions[index])
            if 0 <= (regs[self.ip] + 1) < len(self.instructions):
                regs = t_add_pos(regs, self.ip, 1)
            else:
                break
        return regs[0]

    def part_a(self):
        return self.run((0, 0, 0, 0, 0, 0))

    def part_b(self):
        return self.run((1, 0, 0, 0, 0, 0))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day19)
