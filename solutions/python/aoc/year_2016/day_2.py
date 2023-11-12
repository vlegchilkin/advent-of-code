import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.space import Spacer, C_SIDES


class Year2016Day2(Solution):
    def __init__(self, inp: Input):
        self.moves = inp.get_lines()

    def get_code(self, keypad, start_pos) -> str:
        spacer = Spacer.build(keypad)
        result = ""
        last = start_pos
        for move in self.moves:
            for step in move:
                if (_last := spacer.move(last, C_SIDES[step], cyclic=False)) is not None:
                    last = _last
            result += spacer[last]
        return result

    def part_a(self):
        keypad = Input(0).get_matrix(2)
        return self.get_code(keypad, 1 + 1j)

    def part_b(self):
        keypad = Input(2).get_matrix(2)
        return self.get_code(keypad, 2 + 0j)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day2)
