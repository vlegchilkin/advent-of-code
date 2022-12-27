import math
import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        self.items = inp.get_lists(
            "{{ name }}: capacity {{c|to_int}}, durability {{d|to_int}}, "
            "flavor {{f|to_int}}, texture {{t|to_int}}, calories {{cal|to_int}}"
        )

    def count(self, item_id, spoons_left, total, cal_limit=None):
        if item_id < 0:
            if (cal_limit is not None and total[4] != cal_limit) or min(total[:4]) <= 0:
                return 0
            else:
                return math.prod(total[:4])

        best = 0
        for spoons in range(0 if item_id > 0 else spoons_left, spoons_left + 1):
            new_total = [r + spoons * self.items[item_id][i + 1] for i, r in enumerate(total)]
            best = max(best, self.count(item_id - 1, spoons_left - spoons, new_total, cal_limit))
        return best

    def part_a(self):
        return self.count(len(self.items) - 1, 100, [0, 0, 0, 0, 0])

    def part_b(self):
        return self.count(len(self.items) - 1, 100, [0, 0, 0, 0, 0], 500)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
