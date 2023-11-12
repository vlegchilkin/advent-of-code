import re

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2017Day6(Solution):
    """2017/6: Memory Reallocation"""

    def __init__(self, inp: Input):
        self.banks = inp.get_lines(lambda line: tuple(map(int, re.findall(r"\d+", line))))[0]

    @staticmethod
    def reallocation(banks) -> tuple:
        s = max(banks)
        s_index = banks.index(s)
        result = list(banks)
        result[s_index] = 0
        while s:
            s_index = s_index + 1 if s_index < len(banks) - 1 else 0
            result[s_index] += 1
            s -= 1
        return tuple(result)

    def part_a_b(self):
        banks = self.banks
        visited = {banks: 0}
        while (banks := self.reallocation(banks)) not in visited:
            visited[banks] = len(visited)

        return len(visited), len(visited) - visited[banks]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day6)
