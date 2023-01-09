import copy
import itertools

import pytest

from aoc.space import Spacer, C

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    def __init__(self, inp: Input):
        self.spacer = Spacer.build(inp.get_array(lambda c: "#" if c == "#" else None), ranges=None)
        self.turns = [
            (C.NORTH, [C.NORTH_WEST, C.NORTH, C.NORTH_EAST]),
            (C.SOUTH, [C.SOUTH_WEST, C.SOUTH, C.SOUTH_EAST]),
            (C.WEST, [C.SOUTH_WEST, C.WEST, C.NORTH_WEST]),
            (C.EAST, [C.SOUTH_EAST, C.EAST, C.NORTH_EAST]),
        ]

    def _round(self, round_number, elves) -> bool:
        # first half
        shifted_turns = self.turns[round_number % 4 :] + self.turns[: round_number % 4]
        proposals = {}
        for elf, _ in elves:
            if next(self.spacer.links(elf, has_path=lambda pos: pos in elves), None) is not None:
                for turn in shifted_turns:
                    if next(self.spacer.links(elf, turn[1], has_path=lambda pos: pos in elves), None) is None:
                        turn_ = elf + turn[0]
                        proposals.setdefault(turn_, []).append(elf)
                        break
        # second half
        for proposal, candidates in proposals.items():
            if len(candidates) == 1:
                elves[proposal] = "#"
                del elves[candidates[0]]

        return bool(proposals)

    def part_a(self):
        _elves = copy.deepcopy(self.spacer)
        for r in range(10):
            self._round(r, _elves)

        mm = _elves.minmax()
        return int((mm[1].real - mm[0].real + 1) * (mm[1].imag - mm[0].imag + 1)) - len(_elves)

    def part_b(self):
        _elves = copy.deepcopy(self.spacer)
        for r in itertools.count(0):
            if not self._round(r, _elves):
                return r + 1


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
