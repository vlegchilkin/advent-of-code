import networkx as nx

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Year2017Day12(ISolution):
    """2017/12: Digital Plumber"""

    def __init__(self, inp: Input):
        self.links = inp.get_lists('{{node | to_int}} &lt;-&gt; {{ to_nodes | ORPHRASE | to_int_list(sep=", ")}}')

    def part_a_b(self):
        graph = nx.Graph()
        for _from, to_nodes in self.links:
            for _to in to_nodes:
                graph.add_edge(_from, _to)

        components = list(nx.connected_components(graph))
        zero_group_size = len(next((g for g in components if 0 in g)))
        return zero_group_size, len(components)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day12)
