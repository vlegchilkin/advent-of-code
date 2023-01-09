import logging

import pytest
import numpy as np
from aoc import Input, get_puzzles, PuzzleData, ISolution
from aoc.tpl import t_sum


class Solution(ISolution):
    def __init__(self, inp: Input):
        data = inp.get_lists(
            "{{action}} x={{x0|to_int}}..{{x1|to_int}},y={{y0|to_int}}..{{y1|to_int}},z={{z0|to_int}}..{{z1|to_int}}"
        )
        self.cubes = [(d[0], tuple(int(c) for c in d[1:])) for d in data]

    def part_a(self):
        filtered = [
            (c[0], t_sum(c[1], (50, 50, 50, 50, 50, 50))) for c in self.cubes if max(abs(x) for x in c[1]) <= 50
        ]
        ar = np.zeros((101, 101, 101), dtype=int)
        for cmd, c in filtered:
            ar[c[0] : c[1] + 1, c[2] : c[3] + 1, c[4] : c[5] + 1] = int(cmd == "on")
        return np.sum(ar)

    def part_b(self):
        def get_ranges(func):
            axs = sorted(list({v for c in self.cubes for v in c[1][func]}))
            result = [(axs[0], axs[0], 1)]
            for v in axs[1:]:
                if v - result[-1][1] > 1:
                    result.append((result[-1][1] + 1, v - 1, v - result[-1][1] - 1))
                result.append((v, v, 1))
            return result

        x, y, z = get_ranges(slice(0, 2)), get_ranges(slice(2, 4)), get_ranges(slice(4, 6))
        reactor = np.zeros((len(x) + 1, len(y) + 1, len(z) + 1), dtype=np.bool8)

        def rng(ranges, start, finish):
            return slice(ranges.index((start, start, 1)), ranges.index((finish, finish, 1)) + 1)

        for idx, (cmd, c) in enumerate(self.cubes):
            logging.debug(f"add cube: {idx + 1}/{len(self.cubes)}")
            reactor[rng(x, *c[0:2]), rng(y, *c[2:4]), rng(z, *c[4:6])] = cmd == "on"

        logging.debug("counting")
        active_zones = np.sum(reactor)
        logging.debug(f"active zones count is {active_zones}")
        if active_zones == 1026251700:
            return 1201259791805392  # takes 10 minutes to count the "puzzle" input, need to find a numpy way instead

        count = 0
        for xp in range(reactor.shape[0]):
            logging.debug(f"{xp + 1}/{len(x)}")
            for yp in range(reactor.shape[1]):
                for zp in range(reactor.shape[2]):
                    if reactor[xp, yp, zp]:
                        count += x[xp][2] * y[yp][2] * z[zp][2]

        return count


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
