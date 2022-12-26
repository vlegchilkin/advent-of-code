from itertools import permutations
import re

import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        p = re.compile(r"^(\w+) would (lose|gain) (\d+) happiness units by sitting next to (\w+).$")
        data = [p.match(line).groups() for line in inp.get_lines()]
        self.rules = {(d[0], d[3]): (1 if d[1] == "gain" else -1) * int(d[2]) for d in data}
        self.names = {r[0] for r in self.rules} | {r[1] for r in self.rules}

    def _happiness(self, table) -> int:
        result = 0
        table_size = len(table)

        for i, name in enumerate(table):
            next_person = table[(i + 1) % table_size]
            result += self.rules.get((name, next_person), 0)

            previous_person = table[(i - 1) if i > 0 else table_size - 1]
            result += self.rules.get((name, previous_person), 0)

        return result

    def check_all_permutations(self, names):
        return max([self._happiness(table) for table in permutations(names)])

    def part_a(self):
        return self.check_all_permutations(self.names)

    def part_b(self):
        return self.check_all_permutations(self.names | {None})


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
