import collections as cl
import math
import re
from collections import deque

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    """2016/10: Balance Bots"""

    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    def part_a_b(self):
        def side(s: str) -> tuple[str, int]:
            kind, num = s.split(" ")
            return kind, int(num)

        m = re.compile(r"^bot (\d+) gives low to (.*) and high to (.*)$")
        rules = {
            int(d[0]): (side(d[1]), side(d[2]))
            for d in [m.match(line).groups() for line in self.lines if line.startswith("bot")]
        }

        bots, outputs = cl.defaultdict(deque), cl.defaultdict(list)
        part_a = None

        q = deque([tuple(map(int, re.findall(r"\d+", line))) for line in self.lines if line.startswith("value")])
        while q:
            value, bot_id = q.popleft()
            values = bots[bot_id]
            values.append(value)
            while len(values) >= 2:
                mm = sorted((values.popleft(), values.popleft()))
                if mm == [17, 61]:
                    part_a = bot_id
                for (s_type, s_id), v in zip(rules[bot_id], mm):
                    if s_type == "bot":
                        q.append((v, s_id))
                    else:
                        outputs[s_id].append(v)
        return part_a, math.prod((outputs[i][0] for i in range(3)))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
