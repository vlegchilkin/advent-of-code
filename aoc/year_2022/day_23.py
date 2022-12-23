import numpy as np

from aoc import Input, D, Spacer, t_sum, t_minmax


class Solution:
    def __init__(self, inp: Input, max_rounds=1000):
        self.max_rounds = max_rounds
        inp_arr = inp.get_array({"#": 1, ".": 0})
        self.spacer = Spacer(*t_sum(inp_arr.shape, (2 * max_rounds, 2 * max_rounds)))
        self.elves = {(x + max_rounds, y + max_rounds) for (x, y), value in np.ndenumerate(inp_arr) if value}
        self.turns = [
            (D.NORTH, [D.NORTH_WEST, D.NORTH, D.NORTH_EAST]),
            (D.SOUTH, [D.SOUTH_WEST, D.SOUTH, D.SOUTH_EAST]),
            (D.WEST, [D.SOUTH_WEST, D.WEST, D.NORTH_WEST]),
            (D.EAST, [D.SOUTH_EAST, D.EAST, D.NORTH_EAST]),
        ]

    def _round(self, round_number, elves) -> bool:
        # first half
        shifted_turns = self.turns[round_number % 4 :] + self.turns[: round_number % 4]
        proposals = {}
        for elf in elves:
            if next(self.spacer.get_links(elf, test=lambda pos: pos in elves), None):
                for turn in shifted_turns:
                    if not next(self.spacer.get_links(elf, turn[1], test=lambda pos: pos in elves), None):
                        proposals.setdefault(t_sum(elf, turn[0]), []).append(elf)
                        break
        # second half
        for proposal, candidates in proposals.items():
            if len(candidates) == 1:
                elves.add(proposal)
                elves.remove(candidates[0])

        return bool(proposals)

    def part_a(self):
        _elves = self.elves.copy()
        for r in range(10):
            self._round(r, _elves)

        mm = t_minmax(_elves)
        return (mm[1][1] - mm[0][1] + 1) * (mm[1][0] - mm[0][0] + 1) - len(self.elves)

    def part_b(self):
        _elves = self.elves.copy()
        for r in range(self.max_rounds):
            if not self._round(r, _elves):
                return r + 1


def test_simple():
    solution = Solution(Input(0))
    assert solution.part_a() == 110
    assert solution.part_b() == 20


def test_challenge():
    solution = Solution(Input())
    assert solution.part_a() == 3877
    assert solution.part_b() == 982