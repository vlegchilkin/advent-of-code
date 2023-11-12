from typing import Callable

import pytest
import networkx as nx

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution

TTP_TEMPLATE = "{{ f }} to {{ t }} = {{ length | to_int }}"


class Year2015Day9(Solution):
    def __init__(self, inp: Input):
        self.graph = nx.Graph()
        for o in inp.get_objects(TTP_TEMPLATE):
            self.graph.add_edge(o.f, o.t, weight=o.length)

    def find(self, src: str, not_visited: set, is_better: Callable[[int, int], bool]):
        if not not_visited:
            return 0

        best = None
        for dst in self.graph[src]:
            if dst in not_visited:
                current = self.find(dst, not_visited - {dst}, is_better)
                if current is not None:
                    current += self.graph.get_edge_data(src, dst)["weight"]
                if best is None or current is not None and is_better(best, current):
                    best = current
        return best

    def find_best(self, is_better: Callable[[int, int], bool]):
        nodes = list(self.graph)
        best = None
        for start in self.graph:
            current = self.find(start, set(nodes) - {start}, is_better)
            if best is None or current is not None and is_better(best, current):
                best = current
        return best

    def part_a(self):
        return self.find_best(lambda best, current: current < best)

    def part_b(self):
        return self.find_best(lambda best, current: current > best)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2015Day9)
