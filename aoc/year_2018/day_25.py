import itertools
import re
import networkx as nx

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.tpl import t_dist


class Year2018Day25(Solution):
    """2018/25: Four-Dimensional Adventure"""

    def __init__(self, inp: Input):
        def parse(line):
            return tuple(map(int, re.findall(r"-?\d+", line)))

        self.points = inp.get_lines(parse)

    def part_a(self):
        graph = nx.Graph({p: [] for p in self.points})
        for a, b in itertools.combinations(self.points, 2):
            if t_dist(a, b) <= 3:
                graph.add_edge(a, b)
        return len(list(nx.connected_components(graph)))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day25)
