import copy
import re
import string

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    def __init__(self, inp: Input):
        self.stacks = None
        input_iter = inp.get_iter()
        while (line := next(input_iter, None)) and (line[1] != "1"):
            if not self.stacks:
                self.stacks = [[] for _ in range((len(line) + 1) // 4)]
            for i in range(0, len(self.stacks)):
                if (e := line[i * 4 + 1]) in string.ascii_uppercase:
                    self.stacks[i].insert(0, e)
        next(input_iter)
        r = re.compile(r"^move (\d+) from (\d+) to (\d+)$")
        self.lines = [list(map(int, r.match(line).groups())) for line in input_iter]

    def part_a(self):
        part_a = copy.deepcopy(self.stacks)
        for count, f, t in self.lines:
            part_a[t - 1].extend(reversed(part_a[f - 1][-count:]))
            del part_a[f - 1][-count:]

        return "".join([stack[-1] for stack in part_a if stack])

    def part_b(self):
        part_b = copy.deepcopy(self.stacks)
        for count, f, t in self.lines:
            part_b[t - 1].extend(part_b[f - 1][-count:])
            del part_b[f - 1][-count:]

        return "".join([stack[-1] for stack in part_b if stack])


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
