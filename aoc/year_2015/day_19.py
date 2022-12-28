import copy
import string

import pytest

from aoc import Input, get_puzzles, PuzzleData, algo


class Solution:
    def __init__(self, inp: Input):
        inp_iter = inp.get_iter()
        self.mapping = {}
        self.replacements = {}
        while line := next(inp_iter).strip():
            rule = self._normalize(line.split(" => "))
            self.replacements.setdefault(rule[0], []).append(rule[1])

        for m, v in self.mapping.items():
            if v not in self.replacements:
                self.replacements[v] = []

        self.molecule = self._normalize([next(inp_iter)])[0]

    def get_mapped(self, st) -> str:
        if not st:
            return ""
        if st not in self.mapping:
            x = len(self.mapping)
            if x < 26:
                val = chr(x + ord("A"))
            else:
                val = chr((x - 26) + ord("0"))
            self.mapping[st] = val
        return self.mapping[st]

    def _normalize(self, strs: list[str]) -> list[str]:
        result = []
        for s in strs:
            r = ""
            last = None
            for c in s:
                if c in string.ascii_uppercase:
                    r += self.get_mapped(last)
                    last = c
                else:
                    if c == "e":
                        last = "$"
                    else:
                        last += c
            r += self.get_mapped(last)
            result.append(r)
        return result

    def part_a(self):
        all_possible = set()
        for f, t_list in self.replacements.items():
            for t in t_list:
                for start in range(len(self.molecule) - len(f)):
                    if not self.molecule[start:].startswith(f):
                        continue
                    all_possible.add((self.molecule[:start] + t + self.molecule[start + len(f) :]))

        return len(all_possible)

    def part_b(self):
        base_rules = set(self.replacements)
        rules = copy.deepcopy(self.replacements)

        for rep, val in rules.items():
            if rep != self.mapping["$"]:
                rules[rep].append(rep.lower())

        doubles = {v: rep for rep, val in rules.items() for v in val if len(v) == 2}

        def split(st):
            nonlocal doubles

            if len(st) > 2:
                x = st
                while len(x) != 2:
                    x = split(x[:2]) + (split(x[2:]) if len(x) > 3 else x[2])
                return x

            if st not in doubles:
                x = self.get_mapped(st)
                doubles[st] = x
                rules[x] = [st]

            return doubles[st]

        for rep in list(rules):
            new_val = []
            for v in rules[rep]:
                if len(v) <= 2:
                    new_val.append(v)
                else:
                    new_val.append(split(v))
            rules[rep] = new_val

        molecule = self.molecule.lower()
        rule_weights = {r: 1 for r in base_rules}
        weights, _ = algo.cyk(rules, molecule, rule_weights)
        return weights[self.mapping["$"]]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
