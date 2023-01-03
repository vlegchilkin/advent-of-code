import re
import collections as cls

import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        it = inp.get_iter()
        self.line = next(it)
        next(it)
        self.mapping = {g[0]: g[1] for g in [re.match(r"^(\w+) -> (\w)$", line).groups() for line in it]}

    def _single_round(self, pairs: cls.Counter) -> cls.Counter:
        result = cls.Counter()
        for (l, r), v in pairs.items():
            if c := self.mapping.get(l + r, None):
                result[l + c] += v
                result[c + r] += v
            else:
                result[l + r] = v
        return result

    def _simulate(self, rounds) -> int:
        pairs = cls.Counter(self.line[i - 1 : i + 1] for i in range(1, len(self.line)))

        for _ in range(rounds):
            pairs = self._single_round(pairs)

        counter = cls.Counter()
        for k, v in pairs.items():
            counter[k[0]] += v
        counter[self.line[-1]] += 1
        return max(counter.values()) - min(counter.values())

    def part_a(self):
        return self._simulate(10)

    def part_b(self):
        return self._simulate(40)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
