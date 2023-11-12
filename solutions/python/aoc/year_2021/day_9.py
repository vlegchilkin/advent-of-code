import math
import networkx as nx
import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.space import Spacer, C_BORDERS


class Year2021Day9(Solution):
    def __init__(self, inp: Input):
        self.a = inp.get_array(int)

    def part_a(self):
        spacer = Spacer.build(self.a, directions=C_BORDERS)
        result = 0
        for pos, value in spacer:
            if next(spacer.links(pos, has_path=lambda to_pos, p=pos: spacer.at[p] >= spacer.at[to_pos]), None) is None:
                result += value + 1
        return result

    def part_b(self):
        spacer = Spacer.build(self.a, directions=C_BORDERS)
        graph = nx.Graph()
        for pos, value in spacer:
            if value != 9:
                for link in spacer.links(pos, has_path=lambda to_pos: spacer.at[to_pos] != 9):
                    graph.add_edge(pos, link)

        sizes = sorted(map(len, nx.connected_components(graph)), reverse=True)
        return math.prod(sizes[:3])


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2021Day9)
