import string

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import Spacer
import collections as cl


class Year2023Day3(Solution):
    """2023/3: Gear Ratios"""

    def __init__(self, inp: Input):
        self.arr = inp.get_array(lambda c: c if c != "." else None)

    def part_a_b(self):
        part_a = 0
        spacer = Spacer.build(self.arr)

        def numWithSymbols(r, cs):
            result = 0
            adj = set()
            for j in cs:
                y = r + j * 1j
                result = result * 10 + int(spacer[y])
                for z in spacer.links(y, has_path=lambda p: p in spacer and spacer[p] not in string.digits):
                    adj.add(z)
            return result, adj

        gears = cl.defaultdict(list)
        for row in range(spacer.n):
            j0 = None
            for j1 in range(spacer.m + 1):
                x = row + j1 * 1j
                if x in spacer and spacer[x] in string.digits:
                    if j0 is None:
                        j0 = j1
                elif j0 is not None:
                    num, symbols = numWithSymbols(row, range(j0, j1))
                    if symbols:
                        part_a += num
                        for pos in symbols:
                            if spacer[pos] == '*':
                                gears[pos].append(num)
                    j0 = None

        part_b = 0
        for nums in gears.values():
            if len(nums) == 2:
                part_b += nums[0] * nums[1]

        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2023Day3)
