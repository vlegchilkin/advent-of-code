from itertools import cycle

import pytest
import numpy as np

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import C_MOVES, C, Spacer, C_TURNS


class Year2018Day13(Solution):
    """2018/13: Mine Cart Madness"""

    def __init__(self, inp: Input):
        self.data = inp.get_array()
        self.carts = {}

        for pos, v in np.ndenumerate(self.data):
            if d := C_MOVES.get(v):
                self.data[pos] = "|" if d in {C.NORTH, C.SOUTH} else "-"
                self.carts[pos] = d

    def part_a_b(self):
        spacer = Spacer.build(self.data)
        carts = {complex(*cart): (d, cycle(["L", "F", "R"])) for cart, d in self.carts.items()}

        part_a = None
        for _ in range(1_000_000):  # just to prevent infinite loops
            if len(carts) == 1:
                break
            for cart in sorted(carts.keys(), key=lambda c: (c.real, c.imag)):
                if cart not in carts:
                    continue
                d, it = carts.pop(cart)
                pos = spacer.move(cart, d)
                if pos in carts:
                    if part_a is None:
                        part_a = f"{int(pos.imag)},{int(pos.real)}"
                    del carts[pos]
                    continue

                if (v := spacer[pos]) == "+":
                    d = C_TURNS[d][next(it)]
                elif v == "/":
                    d = {C.EAST: C.NORTH, C.SOUTH: C.WEST, C.NORTH: C.EAST, C.WEST: C.SOUTH}[d]
                elif v == "\\":
                    d = {C.EAST: C.SOUTH, C.SOUTH: C.EAST, C.NORTH: C.WEST, C.WEST: C.NORTH}[d]

                carts[pos] = (d, it)

        assert len(carts) == 1
        last_cart = list(carts)[0]
        part_b = f"{int(last_cart.imag)},{int(last_cart.real)}"
        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day13)
