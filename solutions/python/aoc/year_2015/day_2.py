import itertools

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2015Day2(Solution):
    def __init__(self, inp: Input):
        self.gifts = inp.get_lists("""{{ l | to_int }}x{{ w | to_int }}x{{ h | to_int }}""")

    @staticmethod
    def paper(gift):
        result = sum([2 * c[0] * c[1] for c in itertools.combinations(gift, 2)])
        s = sorted(gift)
        return result + s[0] * s[1]

    @staticmethod
    def ribbon(gift):
        s = sorted(gift)
        return 2 * s[0] + 2 * s[1] + s[0] * s[1] * s[2]

    def part_a(self):
        return sum([self.paper(gift) for gift in self.gifts])

    def part_b(self):
        return sum([self.ribbon(gift) for gift in self.gifts])


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2015Day2)
