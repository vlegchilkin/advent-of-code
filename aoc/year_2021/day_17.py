import re
from typing import Optional, Generator

import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        groups = tuple(map(int, re.findall(r"-?\d+", inp.get_text())))
        self.x_range = groups[0], groups[1]
        self.y_range = groups[2], groups[3]

    def shoot(self, vx, vy) -> Optional[int]:
        x = y = best_y = 0
        while x <= self.x_range[1] and y >= self.y_range[0] and (vx or x >= self.x_range[0]):
            if self.x_range[0] <= x <= self.x_range[1] and self.y_range[0] <= y <= self.y_range[1]:
                return best_y
            if vx:
                x += vx
                vx -= 1
            y += vy
            vy -= 1
            best_y = max(best_y, y)

    def _bruteforce(self) -> Generator[tuple[int, int], None, None]:
        for y in range(-self.y_range[0], self.y_range[0] - 1, -1):
            for x in range(1, self.x_range[1] + 1):
                if (max_height := self.shoot(x, y)) is not None:
                    yield max_height

    def part_a(self):
        return next(self._bruteforce())

    def part_b(self):
        return sum(1 for _ in self._bruteforce())


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
