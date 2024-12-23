import pytest
import collections as cl
import itertools as it
import networkx as nx

from aoc import Input, get_puzzles, PuzzleData, Solution


# from aoc.graph import draw


class Year2024Day23(Solution):
    """2024/23: LAN Party"""

    def __init__(self, inp: Input):
        self.links = inp.get_lines(lambda x: x.split("-"))

    def part_a(self):
        graph = cl.defaultdict(set)
        for _from, _to in self.links:
            graph[_from].add(_to)
            graph[_to].add(_from)

        cliques = set()
        for n1 in graph.keys():
            if n1[0] != 't': continue
            for n2, n3 in it.combinations(graph[n1], 2):
                if n2 in graph[n3]:
                    cliques.add(tuple(sorted([n1, n2, n3])))

        return len(cliques)

    def part_b(self):
        graph = cl.defaultdict(set)
        for _from, _to in self.links:
            graph[_from].add(_to)
            graph[_to].add(_from)

        cliques = {(g,): v for g, v in graph.items()}
        while len(cliques) > 1:
            _cliques = dict()
            for clique, candidates in cliques.items():
                for candidate in candidates:
                    _clique = tuple(sorted(list(clique) + [candidate]))
                    _candidates = candidates.intersection(graph[candidate])
                    _cliques[_clique] = _candidates
            cliques = _cliques

        result = ",".join(list(cliques.keys())[0])
        return result

    def part_b_via_networkx(self) -> str:
        graph = nx.from_edgelist(self.links)
        # draw(graph, "day_23_graph.png")
        cliques = nx.find_cliques(graph)
        result = max(cliques, key=len)
        return ",".join(sorted(result))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2024Day23)
