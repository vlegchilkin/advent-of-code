import pytest
import numpy as np
from numpy import int8

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2016Day16(Solution):
    """2016/16: Dragon Checksum"""

    def __init__(self, inp: Input):
        self.init_bits = np.array([int(b) for b in inp.get_lines()[0]])

    def _checksum(self, disk_size):
        disk = np.zeros(disk_size, dtype=int8)
        next_index = len(self.init_bits)
        disk[:next_index] = self.init_bits
        while next_index < disk_size:
            _len = min(next_index, disk_size - next_index - 1)
            disk[next_index + 1 : next_index + _len + 1] = 1 - np.flip(disk[next_index - _len : next_index])
            next_index += _len + 1

        while len(disk) % 2 == 0:
            disk = 1 - ((disk[::2] + disk[1::2]) % 2)
        return "".join(map(str, disk))

    def part_a(self):
        return self._checksum(272)

    def part_b(self):
        return self._checksum(35651584)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day16)
