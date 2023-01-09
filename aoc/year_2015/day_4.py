from hashlib import md5

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    def __init__(self, inp: Input):
        self.key = inp.get_lines()[0]

    def md5_with_prefix(self, prefix):
        i = 1
        while not md5(f"{self.key}{i}".encode("utf-8")).hexdigest().startswith(prefix):
            i += 1
        return i

    def part_a(self):
        return self.md5_with_prefix("00000")

    def part_b(self):
        return self.md5_with_prefix("000000")


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
