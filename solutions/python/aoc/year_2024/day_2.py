import re
import numpy as np

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2024Day2(Solution):
    """2024/2: Red-Nosed Reports"""

    def __init__(self, inp: Input):
        self.reports = inp.get_lines(lambda s: list(map(int, re.findall(r"\d+", s))))

    @staticmethod
    def _is_safe(report):
        diff = np.diff(report)

        if np.all(diff < 0) or np.all(diff > 0):
            abs_diff = np.absolute(diff)
            return np.all((0 < abs_diff) & (abs_diff < 4))

        return False

    def part_a(self):
        return sum(self._is_safe(report) for report in self.reports)

    def part_b(self):
        safe = 0
        for report in self.reports:
            for i, _ in enumerate(report):
                filtered_report = report[:i] + report[i + 1:]
                if self._is_safe(filtered_report):
                    safe += 1
                    break

        return safe


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2024Day2)
