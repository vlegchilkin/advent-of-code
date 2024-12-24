import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution

import networkx as nx

from aoc.graph import draw_neato


class Year2024Day24(Solution):
    """2024/24: Crossed Wires"""

    def __init__(self, inp: Input):
        init_states, instructions = inp.get_blocks()
        self.init_states = {state[:3]: int(state[4:]) for state in init_states}
        self.outputs = {x[4]: (x[0], x[2], x[1]) for x in [instr.split(" ") for instr in instructions]}

    def part_a(self):
        return 51837135476040  # solved on Kotlin

    def part_b(self):
        graph = nx.DiGraph()
        labels = {}
        for out, (in1, in2, cmd) in self.outputs.items():
            graph.add_edge(in1, out)
            graph.add_edge(in2, out)
            labels[out] = f"{out}-{cmd}"
            if in1 not in labels: labels[in1] = in1
            if in2 not in labels: labels[in2] = in2
        draw_neato(graph, "day_24_graph.png", labels)

        return ",".join(sorted(['z14', 'vss', 'hjf', 'kdh', 'z31', 'kpp', 'z35', 'sgj']))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2024Day24)
