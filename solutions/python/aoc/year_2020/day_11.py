import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2020Day11(Solution):
    """2020/11: Seating System"""

    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    def part_a(self):
        return None

    def part_b(self):
        return None


def test_playground():  # Playground here
    solution = Year2020Day11(Input(0))
    assert solution.part_a() is None
    assert solution.part_b() is None


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2020Day11)
