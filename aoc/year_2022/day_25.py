import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution

SNAFU = "=-012"


class Year2022Day25(Solution):
    def __init__(self, inp: Input):
        self.snafu_numbers = inp.get_lines()

    def _to_snafu(self, number) -> str:
        if number == 0:
            return ""
        return self._to_snafu((number + 2) // 5) + SNAFU[(number + 2) % 5]

    @staticmethod
    def _to_decimal(snafu):
        result, base = 0, 1
        for c in reversed(snafu):
            result += (SNAFU.index(c) - 2) * base
            base *= 5
        return result

    def part_a(self):
        return self._to_snafu(sum(map(self._to_decimal, self.snafu_numbers)))

    def part_b(self):
        return ""


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2022Day25)
