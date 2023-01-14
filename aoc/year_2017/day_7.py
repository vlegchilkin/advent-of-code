import math
import re
from collections import Counter

import pytest
from addict import Dict

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Year2017Day7(ISolution):
    """2017/7: Recursive Circus"""

    def __init__(self, inp: Input):
        r = re.compile(r"(\w+) \((\d+)\)( -> (.*))?")
        groups = inp.get_lines(lambda line: r.match(line).groups())
        self.data = Dict({g[0]: {"weight": int(g[1]), "children": g[3].split(", ") if g[3] else []} for g in groups})

    def part_a_b(self):
        for name, value in self.data.items():
            for child in value.children:
                self.data[child].parent = name

        def recu(node_name):
            _node = self.data[node_name]
            if not (children := _node.children):
                return _node.weight

            child_weights = {c: recu(c) for c in children}

            if len(weights := Counter(child_weights.values())) == 1:
                return math.prod(next(iter(weights.items()))) + _node.weight

            (_, wrong), (_, normal) = sorted((v, k) for k, v in weights.items())
            defect_node = [c for c, v in child_weights.items() if v == wrong][0]
            nonlocal part_b
            part_b = self.data[defect_node].weight + (normal - wrong)
            return _node.weight + len(children) * normal

        part_a = root = next(name for name, value in self.data.items() if "parent" not in value)
        part_b = None
        recu(root)

        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day7)
