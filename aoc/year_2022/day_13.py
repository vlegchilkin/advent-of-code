import json
from functools import cmp_to_key

import math

from aoc import Input


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


def test_simple():
    solution = Solution(Input(0))
    assert solution.part_a() == 13
    assert solution.part_b() == 140


def test_puzzle():
    solution = Solution(Input())
    assert solution.part_a() == 5003
    assert solution.part_b() == 20280
