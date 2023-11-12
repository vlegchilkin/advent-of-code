import pytest
from llist import dllist

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2016Day19(Solution):
    """2016/19: An Elephant Named Joseph"""

    def __init__(self, inp: Input):
        self.n = int(inp.get_lines()[0])

    def part_a(self):
        d = dllist([i for i in range(1, self.n + 1)])
        node = d.first
        while d.first.next:
            d.remove(node.next or d.first)
            node = node.next or d.first
        return node.value

    def part_b(self):
        d = dllist([i for i in range(1, self.n + 1)])
        node, _len, index = d.first, len(d), 0
        while _len > 1:
            idx = (index + (_len // 2)) % _len
            del d[idx]
            _len -= 1
            if node.next:
                node = node.next
                index += 1 if idx > index else 0
            else:
                node = d.first
                index = 0
        return d.first.value


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day19)
