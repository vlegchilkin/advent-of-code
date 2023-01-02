from typing import Tuple

import math
import numpy as np
import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        self.data = [np.array(list(line), dtype=int) for line in inp.get_iter()]

    @staticmethod
    def _to_int(binary_list):
        return int("".join(map(str, binary_list)), 2)

    @staticmethod
    def _get_gr_er_rates(data) -> Tuple[list[int], list[int]]:
        """Returns (gamma rate, epsilon rate) as binary lists"""
        avg = np.average(data, axis=0)
        return [int(e >= 0.5) for e in avg], [int(e < 0.5) for e in avg]

    def part_a(self):
        return math.prod(map(Solution._to_int, self._get_gr_er_rates(self.data)))

    def part_b(self):
        def rating(rate_id) -> int:
            """Oxygen generator rating uses 'gamma rate' (0), CO2 scrubber rating uses 'epsilon rate' (1)"""
            candidates = self.data
            pos = 0
            while len(candidates) > 1 and pos < len(self.data[0]):
                rates = self._get_gr_er_rates(candidates)
                candidates = [r for r in candidates if r[pos] == rates[rate_id][pos]]
                pos += 1

            assert len(candidates) == 1, "In the end, there can be only one. (C) Highlander"
            return self._to_int(candidates[0])

        return rating(0) * rating(1)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
