import itertools

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2016Day9(Solution):
    """2016/9: Explosives in Cyberspace"""

    def __init__(self, inp: Input):
        self.line = inp.get_lines()[0]

    def find_length(self, s, format_version) -> int:
        it = iter(s)
        result = 0
        while (ch := next(it, None)) is not None:
            if ch != "(":
                result += 1
            else:
                marker = "".join(itertools.takewhile(lambda c: c if c != ")" else None, it))
                length, count = map(int, marker.split("x"))
                subs = "".join(next(it) for _ in range(length))
                result += count * (len(subs) if format_version == 1 else self.find_length(subs, format_version))
        return result

    def part_a(self):
        return self.find_length(self.line, 1)

    def part_b(self):
        return self.find_length(self.line, 2)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day9)
