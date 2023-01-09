import functools
import itertools
from collections import deque
from dataclasses import dataclass

import math
import pytest
from llist import dllist

from aoc import Input, get_puzzles, PuzzleData, ISolution


class SnailNum:
    @dataclass
    class Leaf:
        depth: int
        val: int

    def __init__(self, leaves: dllist):
        self.leaves = leaves

    def reduce(self):
        def explode():
            if not (left_bro := next(filter(lambda n: n().depth == 5, self.leaves.iternodes()), None)):
                return

            if n_prev := left_bro.prev:
                n_prev.value.val += left_bro.value.val
            left_bro.value = SnailNum.Leaf(4, 0)

            right_bro = left_bro.next
            if n_next := right_bro.next:
                n_next().val += right_bro().val
            self.leaves.remove(right_bro)
            return True

        def split():
            if not (big_leaf := next(filter(lambda n: n().val > 9, self.leaves.iternodes()), None)):
                return

            self.leaves.insertafter(SnailNum.Leaf(big_leaf().depth + 1, math.ceil(big_leaf().val / 2)), big_leaf)
            big_leaf.value = SnailNum.Leaf(big_leaf().depth + 1, math.floor(big_leaf().val / 2))
            return True

        while explode() or split():
            ...

    def magnitude(self) -> int:
        q = deque()
        for e in self.leaves:
            q.append(e)
            while len(q) > 1 and q[-1].depth == q[-2].depth:
                q[-2].depth -= 1
                q[-2].val = 3 * q[-2].val + 2 * q[-1].val
                q.pop()
        return q[0].val

    @staticmethod
    def add(a: "SnailNum", b: "SnailNum"):
        def clone(leaves):
            return dllist([SnailNum.Leaf(leaf.depth + 1, leaf.val) for leaf in leaves])

        result = SnailNum(clone(a.leaves) + clone(b.leaves))
        result.reduce()
        return result

    @staticmethod
    def parse(number: str) -> "SnailNum":
        data = dllist()
        depth = 0
        for c in number:
            if c in "[]":
                depth += 1 if c == "[" else -1
            elif c.isdigit():
                data.append(SnailNum.Leaf(depth, int(c)))
        return SnailNum(data)

    def __str__(self) -> str:
        return str(self.leaves)

    def __repr__(self) -> str:
        return repr(self.leaves)


class Solution(ISolution):
    def __init__(self, inp: Input):
        self.numbers = list(map(SnailNum.parse, inp.get_lines()))

    def part_a(self):
        return functools.reduce(SnailNum.add, self.numbers).magnitude()

    def part_b(self):
        return max(
            max(SnailNum.add(n1, n2).magnitude(), SnailNum.add(n2, n1).magnitude())
            for n1, n2 in itertools.combinations(self.numbers, 2)
        )


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
