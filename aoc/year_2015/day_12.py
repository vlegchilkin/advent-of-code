import json

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2015Day12(Solution):
    def __init__(self, inp: Input):
        self.data = json.loads(inp.get_text())

    def count(self, data, exclude=None):
        result = 0
        if type(data) == int:
            result = data
        elif type(data) == dict:
            if exclude is None or exclude not in data.values():
                result = sum([self.count(node, exclude) for node in data.values()])
        elif type(data) == list:
            result = sum([self.count(d, exclude) for d in data])

        return result

    def part_a(self):
        return self.count(self.data)

    def part_b(self):
        return self.count(self.data, exclude="red")


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2015Day12)
