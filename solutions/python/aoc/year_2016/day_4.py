import re
from collections import Counter

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2016Day4(Solution):
    def __init__(self, inp: Input):
        self.rooms = [
            (x[0], int(x[1]), x[2]) for x in inp.get_lines(lambda x: re.match(r"^(.*)-(\d+)\[(\w+)]$", x).groups())
        ]

    def part_a(self):
        result = 0
        for room in self.rooms:
            counter = [(count, c) for c, count in Counter(room[0]).items() if c != "-"]
            freq = "".join([e[1] for e in sorted(counter, key=lambda value: (-value[0], ord(value[1])))])
            result += room[1] if freq.startswith(room[2]) else 0
        return result

    def part_b(self):
        for room in self.rooms:
            encrypted = "".join(chr(((ord(c) - ord("a")) + room[1]) % 26 + ord("a")) for c in room[0])
            if encrypted == "northpolehobjecthstorage":
                return room[1]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day4)
