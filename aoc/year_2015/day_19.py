import string

import pytest

from aoc import Input, get_puzzles, PuzzleData


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

        for rep, val in self.replacements.items():
            if rep != self.mapping["$"]:
                self.replacements[rep].append(rep.lower())

        self.key_nodes = set(self.replacements)
        doubles = {}
        for rep, val in self.replacements.items():
            for v in val:
                if len(v) == 2:
                    doubles[v] = rep

        def split(st):
            if len(st) > 2:
                x = split(st[:2]) + split(st[2:])
                if len(x) > 2:
                    x = x[0] + split(x[1:])
                return x

            if st not in doubles:
                x = self.get_mapped(st)
                doubles[st] = x
                self.replacements[x] = [st]

            return doubles[st]

        for rep in list(self.replacements):
            new_val = []
            for v in self.replacements[rep]:
                if len(v) <= 2:
                    new_val.append(v)
                else:
                    new_val.append(split(v))
            self.replacements[rep] = new_val

        self.molecule = self._normalize([next(inp_iter)])[0]

    def cykParse(self, rules, text):
        n = len(text)

        # Initialize the table
        p = [[dict() for _ in range(n)] for _ in range(n)]

        # Filling in the table
        for j in range(0, n):
            # Iterate over the rules
            for lhs, rule in rules.items():
                for rhs in rule:
                    # If a terminal is found
                    if len(rhs) == 1 and rhs[0] == text[j]:
                        p[j][j][lhs] = 0

            for i in range(j, -1, -1):

                # Iterate over the range i to j + 1
                for k in range(i, j):

                    # Iterate over the rules
                    for lhs, rule in rules.items():
                        rule_weight = 1 if lhs in self.key_nodes else 0
                        for rhs in rule:

                            # If a terminal is found
                            if len(rhs) == 2 and rhs[0] in p[i][k] and rhs[1] in p[k + 1][j]:
                                weight = p[i][k][rhs[0]] + p[k + 1][j][rhs[1]] + rule_weight
                                if lhs in p[i][j]:
                                    p[i][j][lhs] = min(p[i][j][lhs], weight)
                                else:
                                    p[i][j][lhs] = weight

        # If word can be formed by rules
        # of given grammar
        return p[0][n - 1][self.mapping["$"]]

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
                    all_possible.add(self.molecule[:start] + t + self.molecule[start + len(f) :])

        return len(all_possible)

    def part_b(self):
        molecule = self.molecule.lower()
        return self.cykParse(self.replacements, molecule)


def test_playground():  # Playground here
    solution = Solution(Input())
    # solution = Solution(Input("a"))
    # assert solution.part_a() == 509
    assert solution.part_b() is None


@pytest.mark.skip(reason="solution template, not a test")
@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
