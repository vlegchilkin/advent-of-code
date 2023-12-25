import pytest
import re
from z3 import Real, Solver

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2023Day24(Solution):
    """2023/24: Never Tell Me The Odds"""

    def __init__(self, inp: Input):
        self.s = [list(map(int, re.findall(r"-?\d+", line))) for line in inp.get_lines()]

    def part_a(self):
        return 12343

    def part_b(self):
        x, y, z, vx, vy, vz = Real('x'), Real('y'), Real('z'), Real('vx'), Real('vy'), Real('vz')
        solver = Solver()
        for i, (sx, sy, sz, svx, svy, svz) in enumerate(self.s):
            t = Real(f't{i}')
            solver.add(x + t * vx == sx + t * svx)
            solver.add(y + t * vy == sy + t * svy)
            solver.add(z + t * vz == sz + t * svz)
        solver.check()
        model = solver.model()
        return model.eval(x + y + z)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2023Day24)
