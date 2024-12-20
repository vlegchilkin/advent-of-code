import math

import pytest
from numpy import inf

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2015Day24(Solution):
    def __init__(self, inp: Input):
        self.weights = sorted(inp.get_lines(int), reverse=True)

    def recu(self, goal, pack, last_index, best) -> (int, int):
        if goal == 0:
            return min(best, (len(pack), math.prod(pack)))

        for i in range(last_index + 1, len(self.weights)):
            if (w := self.weights[i]) > goal:
                continue
            if len(pack) + 1 >= best[0] and w != goal:
                continue
            best = min(best, self.recu(goal - w, pack + [w], i, best))
        return best

    def part_a(self):
        return self.recu(sum(self.weights) // 3, [], -1, (inf, inf))[1]

    def part_b(self):
        return self.recu(sum(self.weights) // 4, [], -1, (inf, inf))[1]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2015Day24)
