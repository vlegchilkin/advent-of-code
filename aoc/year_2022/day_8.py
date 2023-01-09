from itertools import product

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    def __init__(self, inp: Input):
        self.forest = inp.get_lines()
        self.n = len(self.forest)
        self.m = len(self.forest[0])

    def see_side(self, x_list, y_list, height) -> (int, bool):
        trees = 0
        side_view = False
        for x, y in product(x_list, y_list):
            trees += 1
            if self.forest[x][y] >= height:
                break
        else:
            side_view = True
        return trees, side_view

    def look_around(self, x, y) -> (int, bool):
        height = self.forest[x][y]
        n_trees, n_side_view = self.see_side(reversed(range(x)), [y], height)
        s_trees, s_side_view = self.see_side(range(x + 1, self.n), [y], height)
        w_trees, w_side_view = self.see_side([x], reversed(range(y)), height)
        e_trees, e_side_view = self.see_side([x], range(y + 1, self.m), height)

        return n_trees * s_trees * w_trees * e_trees, n_side_view | s_side_view | w_side_view | e_side_view

    def part_a_b(self):
        part_b = 0
        part_a = 0
        for i, j in product(range(self.n), range(self.m)):
            tree_factor, side_visible = self.look_around(i, j)
            if side_visible:
                part_a += 1
            part_b = max(part_b, tree_factor)

        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
