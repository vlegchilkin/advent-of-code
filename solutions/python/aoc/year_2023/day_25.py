import itertools as it
import re

import networkx as nx
import pytest
import pylab as plt

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2023Day25(Solution):
    """2023/25: Snowverload"""

    def __init__(self, inp: Input):
        self.links = {x[0]: x[1:] for x in inp.get_lines(lambda line: re.findall(r"[a-z]{3}", line))}

    @staticmethod
    def _draw(graph):
        pos = nx.spring_layout(graph)
        plt.figure(1, figsize=(48, 48))
        options = {"with_labels": True, "node_size": 1, "font_size": 32}
        nx.draw(graph, pos, **options)
        plt.savefig('day_25_graph.png')

    def part_a(self):
        graph = nx.Graph()
        for src, dst_list in self.links.items():
            for dst in dst_list:
                graph.add_edge(src, dst, capacity=1)

        self._draw(graph)  # first idea was to manually check it on a presentation, and it also works

        for src, dst in it.combinations(graph.nodes, 2):
            cut_value, (a, b) = nx.minimum_cut(graph, src, dst)
            if cut_value == 3:
                return len(a) * len(b)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2023Day25)
