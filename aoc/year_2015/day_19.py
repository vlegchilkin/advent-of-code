from collections import deque

import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        inp_iter = inp.get_iter()
        self.replacements = []
        while line := next(inp_iter).strip():
            self.replacements.append(line.split(" => "))
        self.molecule = next(inp_iter)

    def part_a(self):
        all_possible = set()
        for f, t in self.replacements:
            for start in range(len(self.molecule) - len(f)):
                if not self.molecule[start:].startswith(f):
                    continue
                all_possible.add(self.molecule[:start] + t + self.molecule[start + len(f) :])

        return len(all_possible)

    def recu(self, mol, rev):
        q = deque()
        visited = {mol}
        q.append((mol, 0))
        p = None
        while q and (p := q.popleft())[0] != "e":
            for r in rev:
                if r[0] == "e":
                    if r[1] != p[0]:
                        continue
                    else:
                        return p[1] + 1

                last = 0
                while (finish := p[0].find(r[1], last)) >= 0:
                    s = p[0][:finish] + r[0] + p[0][finish + len(r[1]) :]
                    if s not in visited:
                        visited.add(s)
                        q.append((s, p[1] + 1))
                    last = finish + len(r[1])
        return None

    def part_b(self):
        ending = "Ar"
        subs = []
        last = 0
        while (finish := self.molecule.find(ending, last)) >= 0:
            subs.append(self.molecule[last : finish + len(ending)])
            last = finish + len(ending)
        rev = sorted(self.replacements, key=lambda k: len(k[1]))

        result = 0
        for mol in subs:
            result += self.recu(mol, rev)

        return result


def test_playground():  # Playground here
    solution = Solution(Input())
    assert solution.part_a() == 509
    assert solution.part_b() is None


@pytest.mark.skip(reason="solution template, not a test")
@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
