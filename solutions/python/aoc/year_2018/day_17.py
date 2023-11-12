import re
import sys

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import Spacer, C
from aoc.tpl import t_ranges, t_sum


class Year2018Day17(Solution):
    """2018/17: Reservoir Research"""

    def __init__(self, inp: Input):
        self.data = {}
        for line in inp.get_lines():
            a, b, c = map(int, re.findall(r"\d+", line))
            for x in range(b, c + 1):
                pos = (a, x) if line[0] == "y" else (x, a)
                self.data[pos] = "#"
        self.source = (0, 500)
        self.y_limits, dx = t_ranges(self.data)
        self.x_limits = t_sum(dx, (-1, 1))  # -1/+1 tile for border waterfalls

    def part_a_b(self):
        spacer = Spacer.build(self.data, ranges=((0, self.y_limits[1]), self.x_limits))

        def spread(floor, pos, direction, limit):
            for step in range(1, limit + 1):
                if (left_pos := pos + step * direction) in spacer:
                    return pos + (step - 1) * direction, spacer[left_pos] == "#"
                if (v := floor + step * direction) not in spacer:
                    if not fill(v):
                        return left_pos, False
                elif spacer[v] == "|":
                    return None

        def fill(src: complex):
            if src.real == self.y_limits[1]:
                return False
            if (floor := src + C.SOUTH) not in spacer:
                is_limited = fill(floor)
            else:
                is_limited = spacer[floor] != "|"

            if not is_limited:
                spacer[src] = "|"
                return False

            l_border, l_limited = spread(floor, src, C.WEST, int(src.imag - self.x_limits[0])) or (src, False)
            r_border, r_limited = spread(floor, src, C.EAST, int(self.x_limits[1] - src.imag)) or (src, False)
            character = "~" if l_limited and r_limited else "|"
            p = l_border
            while p != r_border + 1j:
                spacer[p] = character
                p += 1j
            return l_limited and r_limited

        sys.setrecursionlimit(10000)
        fill(complex(*self.source))

        part_a = part_b = 0
        for pos, c in spacer:
            if pos.real >= self.y_limits[0]:
                part_a += c in "~|"
                part_b += c == "~"

        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day17)
