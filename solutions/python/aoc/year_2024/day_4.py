import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import Spacer, C, C_ALL


class Year2024Day4(Solution):
    """2024/4: Ceres Search"""

    def __init__(self, inp: Input):
        self.shirt = inp.get_array()

    def part_a(self):
        spacer = Spacer.build(self.shirt, ranges=None)
        counter = 0
        word = "MAS"
        for pos, symbol in spacer:
            if symbol != "X":
                continue
            directions = C_ALL
            for idx, char in enumerate(word, 1):
                n_directions = []
                for direction in directions:
                    n_pos = pos + direction * idx
                    if spacer.get(n_pos) == char:
                        n_directions.append(direction)
                directions = n_directions
            counter += len(directions)
        return counter

    def part_b(self):
        spacer = Spacer.build(self.shirt, ranges=None)
        directions, x_mas_words = [C.NORTH_EAST, C.NORTH_WEST], {"MAS", "SAM"}
        counter = 0

        for pos, symbol in spacer:
            words = [
                ((spacer.get(pos + d) or ".") + spacer[pos] + (spacer.get(pos - d) or "."))
                for d in directions
            ]
            counter += sum(word in x_mas_words for word in words) == 2

        return counter


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2024Day4)
