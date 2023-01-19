import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import Spacer, C_BORDERS


class Year2016Day13(Solution):
    """2016/13: A Maze of Twisty Little Cubicles"""

    def __init__(self, inp: Input):
        self.number = int(inp.get_lines()[0])
        self.start_pos = 1j + 1
        self.finish_pos = 31j + 39

    def part_a_b(self):
        spacer = Spacer((50, 50), directions=C_BORDERS)

        def is_wall(p):
            x, y = int(p.imag), int(p.real)
            v = bin(x * x + 3 * x + 2 * x * y + y + y * y + self.number)[2:]
            return sum(int(c) for c in v) % 2

        for pos in spacer.iter():
            if not is_wall(pos):
                spacer.at[pos] = 1
        paths, _ = spacer.bfs(self.start_pos)

        distance_to_finish = paths[self.finish_pos][0]
        destinations_in_range_50 = sum(1 for v in paths.values() if v[0] <= 50)
        return distance_to_finish, destinations_in_range_50


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day13)
