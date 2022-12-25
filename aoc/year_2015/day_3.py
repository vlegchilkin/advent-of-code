import pytest

from aoc import Input, get_puzzles, PuzzleData, D, t_sum, D_MOVES


class Solution:
    def __init__(self, inp: Input):
        self.moves = [D_MOVES[c] for c in inp.get_lines()[0]]

    @staticmethod
    def run(moves):
        pos = (0, 0)
        houses = {pos}
        for move in moves:
            pos = t_sum(pos, move)
            houses.add(pos)
        return houses

    def part_a(self):
        return len(self.run(self.moves))

    def part_b(self):
        santa = self.run(self.moves[0::2])
        robo_santa = self.run(self.moves[1::2])
        return len(santa | robo_santa)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
