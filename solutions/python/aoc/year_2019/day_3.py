import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import C_SIDES, c_dist


class Year2019Day3(Solution):
    """2019/3: Crossed Wires"""

    def __init__(self, inp: Input):
        self.lines = inp.get_lines(lambda s: s.split(","))

    @staticmethod
    def build_points(moves):
        result, pos, total_steps = {}, 0j, 0
        for move in moves:
            d, steps = C_SIDES[move[0]], int(move[1:])
            for i in range(steps):
                pos, total_steps = pos + d, total_steps + 1
                if pos not in result:
                    result[pos] = total_steps
        return result

    def part_a(self):
        first, second = map(Year2019Day3.build_points, self.lines)
        common = first.keys() & second.keys()
        return min(map(lambda p: c_dist(0j, p), common))

    def part_b(self):
        first, second = map(Year2019Day3.build_points, self.lines)
        common = first.keys() & second.keys()
        return min(map(lambda p: first[p] + second[p], common))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day3)
