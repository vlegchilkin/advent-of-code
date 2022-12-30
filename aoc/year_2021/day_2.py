import pytest

from aoc import Input, get_puzzles, PuzzleData, D, t_sum, t_koef


class Solution:
    def __init__(self, inp: Input):
        self.actions = inp.get_lists("{{action}} {{steps|to_int}}")
        self.vectors = {
            "forward": D.EAST,
            "down": D.SOUTH,
            "up": D.NORTH,
        }

    def part_a(self):
        pos = (0, 0)
        for action, steps in self.actions:
            vector = t_koef(steps, self.vectors[action])
            pos = t_sum(pos, vector)
        return pos[0] * pos[1]

    def part_b(self):
        pos = aim = (0, 0)
        for action, steps in self.actions:
            vector = t_koef(steps, self.vectors[action])
            if vector[0]:
                aim = t_sum(aim, vector)
            else:
                pos = t_sum(pos, t_sum(vector, t_koef(steps, aim)))
        return pos[0] * pos[1]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
