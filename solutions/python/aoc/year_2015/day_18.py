import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.space import Spacer, IT


class Year2015Day18(Solution):
    def __init__(self, inp: Input):
        self.arr = inp.get_array(lambda c: int(c == "#"))

    @staticmethod
    def switch(spacer):
        result = {}
        for pos, is_on in spacer:
            on_neighbours = sum(spacer.at[p] for p in spacer.links(pos))
            result[pos] = int(on_neighbours == 3 or (on_neighbours == 2 and is_on))
        spacer.at = result

    def part_a(self):
        spacer = Spacer.build(self.arr)
        for _ in range(100):
            self.switch(spacer)
        return sum(spacer.at.values())

    def part_b(self):
        def turn_on_corners():
            for p in spacer.iter(it=IT.CORNERS):
                spacer.at[p] = 1

        spacer = Spacer.build(self.arr)
        turn_on_corners()
        for _ in range(100):
            self.switch(spacer)
            turn_on_corners()

        return sum(spacer.at.values())


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2015Day18)
