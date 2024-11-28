import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import C, C_TURNS, to_str
from aoc.year_2019 import IntcodeComputer


class Year2019Day11(Solution):
    """2019/11: Space Police"""

    def __init__(self, inp: Input):
        self.instructions = list(map(int, inp.get_text().split(",")))

    def _paint(self, start_color) -> dict:
        computer = IntcodeComputer(self.instructions)
        pos, direction = 0j, C.NORTH
        hull = {}
        current_color = start_color
        while response := computer.run([current_color]):
            paint_color, rotation = response
            hull[pos] = paint_color
            direction = C_TURNS[direction]["R" if rotation else "L"]
            pos += direction
            current_color = hull.setdefault(pos, 0)
        return hull

    def part_a(self):
        hull = self._paint(0)
        return len(hull)

    def part_b(self):
        hull = self._paint(1)
        lines = (
            to_str(hull)
            .replace("1", "*")
            .replace("0", ".")
            .replace(".", " ")
        ).splitlines()
        result = "\n".join([line.strip() for line in lines])
        return result


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day11)
