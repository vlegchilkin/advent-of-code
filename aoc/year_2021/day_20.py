import numpy as np
import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        inp_iter = inp.get_iter()
        self.codec = [int(c == "#") for c in next(inp_iter)]
        next(inp_iter)
        self.data = inp.get_array(lambda x: int(x == "#"), lines=list(inp_iter))

    def enhance(self, steps):
        image = {pos: v for pos, v in np.ndenumerate(self.data)}
        for s in range(1, steps + 1):
            inf_value = 0 if self.codec[0] == 0 or s % 2 == 1 else 1
            enhanced = dict()
            for x in range(-s, self.data.shape[0] + s):
                for y in range(-s, self.data.shape[1] + s):
                    value = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            value = value * 2 + image.get((x + i, y + j), inf_value)
                    enhanced[(x, y)] = self.codec[value]
            image = enhanced
        return image

    def part_a(self):
        return sum(self.enhance(2).values())

    def part_b(self):
        return sum(self.enhance(50).values())


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
