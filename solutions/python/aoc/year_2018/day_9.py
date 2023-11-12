import re
from itertools import cycle

import pytest
from llist import dllist

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2018Day9(Solution):
    """2018/9: Marble Mania"""

    def __init__(self, inp: Input):
        def parse(line):
            return tuple(map(int, re.match(r"^(\d+) players; last marble is worth (\d+) points$", line).groups()))

        self.players, self.n = inp.get_lines(parse)[0]

    @staticmethod
    def run(players, n):
        game, scores = dllist([0]), [0] * players
        turns = cycle(i for i in range(players))
        pos = game.first
        for x in range(1, n + 1):
            player = next(turns)
            if x % 23 == 0:
                for _ in range(7):
                    pos = pos.prev or game.last
                scores[player] += x + pos.value
                _pos = pos.next or game.first
                game.remove(pos)
                pos = _pos
            else:
                pos = pos.next or game.first
                pos = game.insertafter(x, pos)
        return max(scores)

    def part_a(self):
        return self.run(self.players, self.n)

    def part_b(self):
        return self.run(self.players, self.n * 100)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day9)
