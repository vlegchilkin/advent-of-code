import pytest

from aoc import Input, get_puzzles, PuzzleData

SNAFU = ["=", "-", "0", "1", "2"]


class Solution:
    def __init__(self, inp: Input):
        self.snafu_numbers = inp.get_lines()
        self.limits = []
        x, b = 2, 1
        while len(self.limits) < 21:
            self.limits.append(x)
            b *= 5
            x += 2 * b

    def _to_snafu_arr(self, number: int) -> list[int]:
        pos, base = 0, 1
        while self.limits[pos] < abs(number):
            pos += 1
            base *= 5

        if pos == 0:
            return [number] + [0] * (len(self.limits) - 1)

        for i in range(-2, 3):
            if -self.limits[pos - 1] <= (remains := number - i * base) <= self.limits[pos - 1]:
                result = self._to_snafu_arr(remains)
                result[pos] = i
                return result

    def _to_snafu(self, number) -> str:
        snafu_arr = self._to_snafu_arr(number)
        snafu_arr.reverse()
        for i in range(len(self.limits)):
            if snafu_arr[i] == 0:
                continue
            return "".join([SNAFU[c + 2] for c in snafu_arr[i:]])

    @staticmethod
    def _to_decimal(snafu):
        result, base = 0, 1
        for c in reversed(snafu):
            result += (SNAFU.index(c) - 2) * base
            base *= 5
        return result

    def part_a(self):
        return self._to_snafu(sum([self._to_decimal(snafu) for snafu in self.snafu_numbers]))

    def part_b(self):
        return ""


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
