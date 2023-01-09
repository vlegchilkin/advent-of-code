from functools import cache
import networkx as nx
import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution

TTP_TEMPLATE = """\
Valve {{ src }} has flow rate={{ rate | to_int }}; \
{{ ignore(r"tunnel(s)? lead(s)? to valve(s)?") }} {{dst | ORPHRASE | split(", ")}}
"""


class Solution(ISolution):
    def __init__(self, inp: Input):
        input_data = {d.src: (d.rate, d.dst) for d in inp.get_objects(TTP_TEMPLATE)}
        keys = sorted(input_data)
        self.rates = [input_data[k][0] for k in keys]
        self.closed_valves = [valve for valve, rate in enumerate(self.rates) if rate > 0]

        graph = nx.Graph([(key, dst) for key, value in input_data.items() for dst in value[1]])
        distances = nx.floyd_warshall(graph)
        self.costs = [[int(distances[k][v]) + 1 for v in keys] for k in keys]

    @cache
    def f(self, valves_state, src_valve, time, time_next: int) -> int:
        if not valves_state:
            return 0
        best = self.f(valves_state, 0, time_next, 0) if time_next else 0

        for dst_valve in self.closed_valves:
            if not ((1 << dst_valve) & valves_state):
                continue
            if (ti := time - self.costs[src_valve][dst_valve]) > 0:
                _closed_valves = valves_state - (1 << dst_valve)
                best = max(best, ti * self.rates[dst_valve] + self.f(_closed_valves, dst_valve, ti, time_next))

        return best

    def part_a(self):
        return self.f(sum(1 << valve for valve in self.closed_valves), 0, 30, 0)

    def part_b(self):
        return self.f(sum(1 << valve for valve in self.closed_valves), 0, 26, 26)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
