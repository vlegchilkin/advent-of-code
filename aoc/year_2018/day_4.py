import collections
import re

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2018Day4(Solution):
    """2018/4: Repose Record"""

    def __init__(self, inp: Input):
        def parse(line):
            return re.match(r"^\[(.*)] (.*)$", line).groups()

        self.records = sorted(inp.get_lines(parse))

    def get_guards_asleep(self) -> dict[int, list[tuple[int, int]]]:
        periods = collections.defaultdict(list)
        guard_id, sleep_from = None, None

        def offset(dt):
            return int(dt[-2:])

        for t, action in self.records:
            if action.startswith("Guard"):
                guard_id = int(re.match(r"^Guard #(\d+) begins shift$", action).groups()[0])
            elif action == "falls asleep":
                sleep_from = offset(t)
            else:
                sleep_to = offset(t)
                periods[guard_id].append((sleep_from, sleep_to))

        return periods

    @staticmethod
    def most_sleep_minute(periods: list[tuple[int, int]]):
        return max((sum(a <= t < b for a, b in periods), t) for t in range(0, 60))

    def part_a(self):
        guards_asleep = self.get_guards_asleep()

        _, guard_id = max((sum(b - a for a, b in periods), _id) for _id, periods in guards_asleep.items())
        _, minute = self.most_sleep_minute(guards_asleep[guard_id])
        return guard_id * minute

    def part_b(self):
        guards_asleep = self.get_guards_asleep()

        (_, minute), guard_id = max((self.most_sleep_minute(periods), _id) for _id, periods in guards_asleep.items())
        return guard_id * minute


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day4)
