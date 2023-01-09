import itertools
import logging
import re
from collections import deque
from dataclasses import dataclass

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution
from aoc.tpl import t_sub, t_sum, t_dist


def trans_coordinates():
    """24 possible coordinate translations for 3d space"""
    result = []
    for x, y, z in [(1, 2, 3), (2, 3, 1), (3, 1, 2)]:
        result += [(x, y, z), (z, y, -x), (-x, y, -z), (-z, y, x), (z, -y, x), (x, -y, -z), (-z, -y, -x), (-x, -y, z)]
    return result


def possible_rotations(s: set[tuple]) -> list[set[tuple]]:
    """translate points to all possible space coordinates rotation"""

    def translate(t, pos: tuple):
        return tuple(pos[abs(v) - 1] * (-1 if v < 0 else 1) for v in t)

    return [{translate(trans, pos) for pos in s} for trans in trans_coordinates()]


class Solution(ISolution):
    def __init__(self, inp: Input):
        self.scanner_beacons = {}
        for block in inp.get_blocks():
            scan_id = int(re.match(r"^--- scanner (\d+) ---$", block[0]).groups()[0])
            self.scanner_beacons[scan_id] = {tuple(map(int, b.split(","))) for b in block[1:]}

    @dataclass
    class Scanner:
        position: tuple[int, int, int]
        beacons: set[tuple[int, int, int]]

    def resolve_in_space(self) -> dict[int, Scanner]:
        scanner_rotations = {s_id: possible_rotations(beacons) for s_id, beacons in self.scanner_beacons.items()}

        def get_possible_shift(real_space: set[tuple], shifted: set[tuple]) -> Solution.Scanner:
            for a in real_space:
                for b in shifted:
                    zero = t_sub((0, 0, 0), t_sub(b, a))
                    zero_shifted = {t_sum(s, zero) for s in shifted}
                    if len(real_space.intersection(zero_shifted)) >= 12:
                        return Solution.Scanner(zero, zero_shifted)

        # align space coordinates to the first scanner position for all others
        first = next(iter(self.scanner_beacons))
        resolved = {first: Solution.Scanner((0, 0, 0), self.scanner_beacons[first])}
        q = deque([first])
        while q:
            logging.debug(f"{len(resolved)}/{len(self.scanner_beacons)} resolved")
            visible_beacons = resolved[q.popleft()].beacons
            for scan_id, possible_beacons in scanner_rotations.items():
                if scan_id not in resolved:
                    for beacons in possible_beacons:
                        if resolved_scanner := get_possible_shift(visible_beacons, beacons):
                            resolved[scan_id] = resolved_scanner
                            q.append(scan_id)
                            break

        return resolved

    def part_a_b(self):
        scanners = self.resolve_in_space()
        part_a = len(set().union(*[v.beacons for v in scanners.values()]))

        part_b = 0
        for x, y in itertools.combinations([v.position for v in scanners.values()], 2):
            part_b = max(part_b, t_dist(x, y))

        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
