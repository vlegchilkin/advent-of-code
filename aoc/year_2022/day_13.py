import json
from functools import cmp_to_key

import math
import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        self.lists = [json.loads(line) for line in inp.get_iter() if line]

    @staticmethod
    def cmp(left, right) -> int:
        l_int, r_int = isinstance(left, int), isinstance(right, int)
        if l_int and r_int:
            return left - right

        left = [left] if l_int else left
        right = [right] if r_int else right

        for left_v, right_v in zip(left, right):
            if c := Solution.cmp(left_v, right_v):
                return c

        return len(left) - len(right)

    def part_a(self) -> int:
        part_a = 0
        for i in range(0, len(self.lists), 2):
            if Solution.cmp(self.lists[i], self.lists[i + 1]) < 0:
                part_a += i // 2 + 1
        return part_a

    def part_b(self) -> int:
        markers = [[[2]], [[6]]]
        lists = sorted(self.lists + markers, key=cmp_to_key(Solution.cmp))
        return math.prod([(i + 1) for i, v in enumerate(lists) if v in markers])


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
