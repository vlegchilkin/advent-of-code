import copy
import string

import pytest

from aoc import Input, get_puzzles, PuzzleData, algo, ISolution


class Solution(ISolution):
    def __init__(self, inp: Input):
        inp_iter = inp.get_iter()
        self.mapping = {}
        self.replacements = self._parse_replacements(inp_iter)
        self.molecule = self._normalize_elements([next(inp_iter)])[0]

    def _mapped(self, element) -> str:
        if element not in self.mapping:
            self.mapping[element] = chr(len(self.mapping) + ord("A"))
        return self.mapping[element]

    def _parse_replacements(self, inp_iter) -> dict:
        replacements = {}
        while line := next(inp_iter).strip():
            rule = self._normalize_elements(line.split(" => "))
            replacements.setdefault(rule[0], []).append(rule[1])

        for m, v in self.mapping.items():
            if v not in replacements:
                replacements[v] = []
        return replacements

    def _normalize_elements(self, strs: list[str]) -> list[str]:
        result = []
        for s in strs:
            r = ""
            element = None
            for c in s + "\n":
                if c in string.ascii_uppercase + "\n":
                    r += self._mapped(element) if element else ""
                    element = c
                else:
                    if c == "e":
                        element = "$"
                    else:
                        element += c
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
        rules = copy.deepcopy(self.replacements)

        for rep, val in rules.items():
            if rep != self.mapping["$"]:
                rules[rep].append(rep.lower())

        rules = algo.make_cnf(rules)

        molecule = self.molecule.lower()
        rule_weights = {r: 1 for r in set(self.replacements)}
        weights, _ = algo.cyk(rules, molecule, rule_weights)
        return weights[self.mapping["$"]]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
