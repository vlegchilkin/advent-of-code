import pytest
import numpy as np
from numpy import Inf

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2018Day11(Solution):
    """2018/11: Chronal Charge"""

    def __init__(self, inp: Input):
        self.serial = inp.get_lines(int)[0]

    def part_a_b(self):
        a = np.ndarray((300, 300), dtype=int)
        for i in range(300):
            for j in range(300):
                rack_id = (j + 1) + 10
                a[i, j] = int(str((rack_id * (i + 1) + self.serial) * rack_id)[-3]) - 5

        def find(s) -> tuple[int, tuple[int, int]]:
            result = (-Inf, None)
            for i in range(300 - s + 1):
                for j in range(300 - s + 1):
                    result = max(result, (np.sum(a[i : i + s, j : j + s]), (j + 1, i + 1)))
            return result

        _, (x, y) = find(3)
        part_a = f"{x},{y}"

        # noinspection PyTupleAssignmentBalance
        _, (x, y), size = max((*find(size), size) for size in range(1, 300))
        part_b = f"{x},{y},{size}"

        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day11)
