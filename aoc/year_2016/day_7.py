import re

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    """2016/7: Internet Protocol Version 7"""

    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    def _get_nets(self) -> list[(set[str], set[str])]:
        """returns hyper and super nets"""
        nets = []
        for line in self.lines:
            hyper_sequences = {g for g in re.findall(r"\[(\w+)]", line)}
            super_sequences = set(re.split(r"\[\w+]", line))
            nets.append((hyper_sequences, super_sequences))
        return nets

    def part_a(self):
        def has_abba(sequences: set[str]) -> bool:
            for seq in sequences:
                for i in range(len(seq) - 3):
                    if seq[i] != seq[i + 1] and seq[i] == seq[i + 3] and seq[i + 1] == seq[i + 2]:
                        return True
            return False

        return sum(not has_abba(h) and has_abba(s) for h, s in self._get_nets())

    def part_b(self):
        result = 0
        for hyper_sequences, super_sequences in self._get_nets():
            possible_aba = set()
            for seq in hyper_sequences:
                for i in range(len(seq) - 2):
                    if seq[i] != seq[i + 1] and seq[i] == seq[i + 2]:
                        possible_aba.add(seq[i + 1] + seq[i] + seq[i + 1])

            result += any(s for s in super_sequences if any(aba for aba in possible_aba if s.find(aba) >= 0))
        return result


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
