import ast

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    def part_a(self):
        result = 0
        for line in self.lines:
            unescaped = ast.literal_eval(line)
            result += len(line) - len(unescaped)
        return result

    @staticmethod
    def _escape(line: str):
        value = line.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{value}"'

    def part_b(self):
        result = 0
        for line in self.lines:
            escaped = self._escape(line)
            result += len(escaped) - len(line)
        return result


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
