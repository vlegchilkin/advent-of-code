import re
from operator import mul

import pytest
import collections as cl
import functools as ft
from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2023Day2(Solution):
    """2023/2: Cube Conundrum"""

    def __init__(self, inp: Input):
        r = re.compile(r"^Game (\d+): (.*)$")
        data = inp.get_lines(lambda line: r.match(line).groups())

        def parse(game: str):
            result = []
            for s in game.split("; "):
                x = {}
                for cubes in s.split(", "):
                    a, b = cubes.split(" ")
                    x[b] = int(a)
                result.append(x)
            return result

        self.games = {int(k): parse(v) for k, v in data}

    def part_a(self):
        limits = {"red": 12, "green": 13, "blue": 14}
        result = 0
        for game_id, game in self.games.items():
            for s in game:
                if any(limits[color] < count for color, count in s.items()):
                    break
            else:
                result += game_id
        return result

    def part_b(self):
        total = 0
        for game in self.games.values():
            max_by_color = cl.defaultdict(int)
            for s in game:
                for color, count in s.items():
                    max_by_color[color] = max(max_by_color[color], count)
            total += ft.reduce(mul, max_by_color.values())
        return total


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2023Day2)
