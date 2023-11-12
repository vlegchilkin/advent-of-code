import itertools
import dataclasses as dc

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2016Day15(Solution):
    """2016/15: Timing is Everything"""

    @dc.dataclass()
    class Disk:
        offset: int
        positions: int
        init_pos: int

    def __init__(self, inp: Input):
        self.disks = inp.get_dc_list(
            "Disc #{{offset|to_int}} has {{positions|to_int}} positions; "
            "at time=0, it is at position {{init_pos|to_int}}.",
            Year2016Day15.Disk,
        )

    @staticmethod
    def find_time(disks):
        for time in itertools.count():
            if all((time + d.init_pos + d.offset) % d.positions == 0 for d in disks):
                return time

    def part_a(self):
        return self.find_time(self.disks)

    def part_b(self):
        return self.find_time(self.disks + [Year2016Day15.Disk(len(self.disks) + 1, 11, 0)])


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day15)
