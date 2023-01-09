from collections import deque

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    def __init__(self, inp: Input):
        self.input_values = [int(line) for line in inp.get_lines()]

    class Mixer:
        def __init__(self, input_values, key=1):
            self.data = deque([(i, line * key) for i, line in enumerate(input_values)])
            self.n = len(input_values)

        def mix(self, steps=1) -> int:
            for _ in range(steps):
                for i in range(self.n):
                    pos = next(index for index, el in enumerate(self.data) if el[0] == i)
                    item = self.data[pos]
                    del self.data[pos]
                    new_pos = (pos + item[1]) % (self.n - 1)
                    self.data.insert(new_pos, item)

            return self._grove_coordinates()

        def _grove_coordinates(self) -> int:
            pos = next(index for index, el in enumerate(self.data) if el[1] == 0)
            return sum([self.data[(pos + offset) % self.n][1] for offset in [1000, 2000, 3000]])

    def part_a(self):
        return self.Mixer(self.input_values).mix()

    def part_b(self):
        return self.Mixer(self.input_values, key=811589153).mix(steps=10)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
