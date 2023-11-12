import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2019Day4(Solution):
    """2019/4: Secure Container"""

    def __init__(self, inp: Input):
        self.lo, self.hi = inp.get_lines(lambda s: tuple(map(int, s.split("-"))))[0]

    @staticmethod
    def is_correct(password, match_only_double=False):
        last, streak = 10, 0
        have_repeats = False

        while password:
            current = password % 10
            if current > last:
                return False
            elif current == last:
                streak += 1
            else:
                have_repeats |= bool(streak == 1 if match_only_double else streak)
                streak = 0
            last = current
            password //= 10

        have_repeats |= bool(streak == 1 if match_only_double else streak)

        return have_repeats

    def part_a(self):
        return sum(map(Year2019Day4.is_correct, range(self.lo, self.hi + 1)))

    def part_b(self):
        return sum(Year2019Day4.is_correct(num, match_only_double=True) for num in range(self.lo, self.hi + 1))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day4)
