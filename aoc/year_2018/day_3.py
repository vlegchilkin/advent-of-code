import re
import numpy as np

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2018Day3(Solution):
    """2018/3: No Matter How You Slice It"""

    def __init__(self, inp: Input):
        def parse(line):
            return tuple(map(int, re.match(r"^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$", line).groups()))

        self.rectangles = {_id: ((x, y), (w, h)) for _id, x, y, w, h in inp.get_lines(parse)}

    def part_a_b(self):
        area = np.zeros((1000, 1000), dtype=int)
        for (x, y), (w, h) in self.rectangles.values():
            area[x : x + w, y : y + h] += 1

        part_a = len(area[area >= 2])
        part_b = None
        for _id, ((x, y), (w, h)) in self.rectangles.items():
            if np.all(area[x : x + w, y : y + h] == 1):
                part_b = _id

        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day3)
