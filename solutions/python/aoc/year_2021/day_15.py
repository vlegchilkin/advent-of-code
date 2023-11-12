import pytest
import numpy as np
import networkx as nx

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.space import Spacer, C_BORDERS, minmax


class Year2021Day15(Solution):
    def __init__(self, inp: Input):
        self.data = inp.get_array(int)

    @staticmethod
    def shortest_path(data: np.ndarray):
        spacer = Spacer.build(data, directions=C_BORDERS)
        g = spacer.to_digraph(weight=lambda _, dst: dst)
        start, finish = minmax(spacer.at.keys())
        return nx.shortest_path_length(g, start, finish, weight="weight")

    def part_a(self):
        return self.shortest_path(self.data)

    def part_b(self):
        factor = 5
        n, m = self.data.shape
        data = np.ndarray(shape=(n * factor, m * factor), dtype=int)
        for i in range(factor):
            for j in range(factor):
                data[i * n : (i + 1) * n, j * m : (j + 1) * m] = (self.data + i + j - 1) % 9 + 1
        return self.shortest_path(data)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2021Day15)
