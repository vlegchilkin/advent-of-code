import re
import numpy as np

import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        line_pattern = re.compile(r"^(.*) -> ([a-z]+)$")
        data = [line_pattern.match(line).groups() for line in inp.get_lines()]
        self.rules = {d[1]: d[0].split(" ") for d in data}

    def _solve(self, rules, wire):
        if type(wire) == np.uint16:
            return wire

        if wire not in rules:
            return np.uint16(wire)

        if type(rule := rules[wire]) == np.uint16:
            return rule

        if len(rule) == 1:  # assignment
            value = self._solve(rules, rule[0])
        elif len(rule) == 2:  # NOT
            value = ~self._solve(rules, rule[1])
        else:
            left = self._solve(rules, rule[0])
            right = self._solve(rules, rule[2])
            match rule[1]:
                case "AND":
                    value = left & right
                case "OR":
                    value = left | right
                case "LSHIFT":
                    value = left << right
                case "RSHIFT":
                    value = left >> right
                case _:
                    raise ValueError(f"Non-Supported operation: {rule[1]}")
        rules[wire] = value
        return value

    def part_a(self):
        return self._solve(self.rules.copy(), "a")

    def part_b(self):
        rules = self.rules.copy()
        rules["b"] = [str(self.part_a())]
        return self._solve(rules, "a")


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
