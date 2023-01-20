import itertools
import re
import string
from typing import Optional

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2018Day7(Solution):
    """2018/7: The Sum of Its Parts"""

    def __init__(self, inp: Input):
        def parse(line):
            return re.match(r"^Step (\w) must be finished before step (\w) can begin.$", line).groups()

        self.rules = inp.get_lines(parse)

    def part_a(self):
        rules = self.rules
        available = sorted(list(set().union(*((a, b) for a, b in rules))))
        result = ""
        while available:
            for c in available:
                if not any(f for f, t in rules if t == c):
                    result += c
                    rules = [r for r in rules if r[0] != c]
                    available.remove(c)
                    break
        return result

    def part_b(self):
        rules = self.rules
        available: list[str] = sorted(list(set().union(*((a, b) for a, b in rules))))
        workers: list[Optional[tuple[str, int]]] = [None, None, None, None, None]

        def assign_work():
            for c in available:
                if all(workers):
                    break
                if any(c for f, t in rules if t == c):
                    continue
                for i, w in enumerate(workers):
                    if w is None:
                        workers[i] = (c, 60 + string.ascii_uppercase.index(c) + 1)
                        available.remove(c)
                        break

        def release_work():
            for i, w in enumerate(workers):
                if w is None:
                    continue
                if w[1] > 1:
                    workers[i] = (w[0], w[1] - 1)
                else:
                    nonlocal rules
                    rules = [r for r in rules if r[0] != w[0]]
                    workers[i] = None

        for time in itertools.count():
            release_work()
            if not any(workers) and not available:
                return time
            assign_work()


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day7)
