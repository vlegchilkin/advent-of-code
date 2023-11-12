import itertools
import re

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2017Day13(Solution):
    """2017/13: Packet Scanners"""

    def __init__(self, inp: Input):
        self.scanners = {
            x[0]: x[1] for x in inp.get_lines(lambda line: list(map(int, re.match(r"^(\d+): (\d+)", line).groups())))
        }

    def part_a_b(self):
        def get_blocked_by(offset, fail_first=False) -> list[tuple[int, int]]:
            result = []
            for t, n in self.scanners.items():
                if (offset + t) % ((n - 1) * 2) == 0:
                    result.append((t, n))
                    if fail_first:
                        break
            return result

        part_a = sum(t * n for t, n in get_blocked_by(0))
        part_b = next(offs for offs in itertools.count() if not get_blocked_by(offs, True))

        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day13)
