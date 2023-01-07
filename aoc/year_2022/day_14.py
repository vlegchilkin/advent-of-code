import numpy as np
import pytest

from aoc import Input, get_puzzles, PuzzleData
from aoc.space import C, Spacer

DIRECTIONS = [C.SOUTH, C.SOUTH_WEST, C.SOUTH_EAST]


class Solution:
    def __init__(self, inp: Input):
        lines = inp.get_lines()
        self.ar = np.empty(shape=(1000, 1000), dtype=object)
        max_row = 0
        for line in lines:
            points = [[int(x) for x in reversed(step.split(","))] for step in line.split(" -> ")]
            for i in range(1, len(points)):
                s, t = sorted([points[i - 1], points[i]])
                self.ar[s[0] : t[0] + 1, s[1] : t[1] + 1] = 1
                max_row = max(max_row, t[0])

        self.floor = max_row + 2
        self.ar[self.floor, :] = 1

    def part_a_b(self) -> (int, int):
        spacer = Spacer.build(self.ar, directions=DIRECTIONS)

        def drop(pos, limit):
            if pos in spacer:
                return False

            while next_pos := next(spacer.links(pos, has_path=lambda p: p not in spacer and p.real <= limit), None):
                pos = next_pos

            if pos.real < limit:
                spacer.at[pos] = 2
                return True

        source = 500j
        count = 0
        while drop(source, self.floor - 2):
            count += 1
        part_a = count

        while drop(source, self.floor):
            count += 1
        return part_a, count


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
