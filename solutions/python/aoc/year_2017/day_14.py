import pytest
import networkx as nx

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import Spacer, C_BORDERS
from aoc.year_2017.day_10 import Year2017Day10


class Year2017Day14(Solution):
    """2017/14: Disk Defragmentation"""

    def __init__(self, inp: Input):
        self.key = inp.get_lines()[0]

    def part_a_b(self):
        def decode(_h: str):
            result = ""
            for c in _h:
                result += bin("0123456789abcdef".index(c))[2:].zfill(4)
            return result

        spacer = Spacer((128, 128), directions=C_BORDERS)
        for i in range(128):
            _hash = Year2017Day10.knot_hash(f"{self.key}-{i}")
            for j, value in enumerate(decode(_hash)):
                if value == "1":
                    spacer[complex(i, j)] = 1

        graph = spacer.to_digraph().to_undirected()
        components = list(nx.connected_components(graph))

        return len(graph.nodes), len(components)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day14)
