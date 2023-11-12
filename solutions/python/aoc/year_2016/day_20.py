import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2016Day20(Solution):
    """2016/20: Firewall Rules"""

    def __init__(self, inp: Input):
        self.black_list = inp.get_lines(lambda v: tuple(map(int, v.split("-"))))

    def part_a_b(self):
        last = -1
        part_a = None
        part_b = 0
        for _from, _to in sorted(self.black_list):
            if _from > last + 1:
                if part_a is None:
                    part_a = last + 1
                part_b += _from - last - 1
            last = max(last, _to)

        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day20)
