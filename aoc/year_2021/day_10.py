from collections import deque

import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        self.lines = inp.get_lines()
        self.costs = {"(": 1, ")": 3, "[": 2, "]": 57, "{": 3, "}": 1197, "<": 4, ">": 25137}
        self.pairs = "{}()[]<>"

    def parse(self, line) -> (int, int):
        """Returns (corrupted costs, incomplete costs)"""
        s = deque()
        for c in line:
            if (pos := self.pairs.index(c)) % 2 == 1:
                if s.pop() != self.pairs[pos - 1]:
                    return self.costs[c], 0
            else:
                s.append(c)

        total = 0
        for v in reversed(s):
            total = 5 * total + self.costs[v]
        return 0, total

    def part_a(self):
        return sum(self.parse(line)[0] for line in self.lines)

    def part_b(self):
        incomplete = sorted(filter(bool, [self.parse(line)[1] for line in self.lines]))
        return incomplete[len(incomplete) // 2]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
