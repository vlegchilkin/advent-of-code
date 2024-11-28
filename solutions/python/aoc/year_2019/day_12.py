import math
import re
import itertools as it

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.tpl import t_sub, t_sum
import dataclasses as dc

DIMENSION = 3


@dc.dataclass
class Moon:
    pos: tuple[int, ...]
    vel: tuple[int, ...]


class Year2019Day12(Solution):
    """2019/12: The N-Body Problem"""

    def __init__(self, inp: Input):
        self.moon_coords = inp.get_lines(lambda line: tuple(map(int, re.findall(r"-?\d+", line))))

    @staticmethod
    def one_step_emulation(moons):
        for a_idx, b_idx in it.combinations(moons.keys(), 2):
            a, b = moons[a_idx], moons[b_idx]
            x = tuple(-1 if axis < 0 else 1 if axis > 0 else 0 for axis in t_sub(b.pos, a.pos))
            a.vel = t_sum(a.vel, x)
            b.vel = t_sub(b.vel, x)
        for moon in moons.values():
            moon.pos = t_sum(moon.pos, moon.vel)

    def part_a(self):
        moons = {idx: Moon(coord, (0,) * DIMENSION) for idx, coord in enumerate(self.moon_coords)}

        for s in range(1000):
            self.one_step_emulation(moons)

        def energy(value):
            return sum(abs(v) for v in value)

        total = sum(energy(moon.pos) * energy(moon.vel) for moon in moons.values())
        return total

    def part_b(self):
        moons = {idx: Moon(coord, (0,) * DIMENSION) for idx, coord in enumerate(self.moon_coords)}

        cycle_len: list[int | None] = [None] * DIMENSION
        axis_snapshots = [set() for _ in range(DIMENSION)]

        for step in range(1_000_000_000):
            for axis in range(DIMENSION):
                if cycle_len[axis] is not None:
                    continue

                axis_snapshot = tuple((moon.pos[axis], moon.vel[axis]) for moon in moons.values())
                snapshots = axis_snapshots[axis]
                if axis_snapshot not in snapshots:
                    snapshots.add(axis_snapshot)
                else:
                    cycle_len[axis] = step

            if all(cycle is not None for cycle in cycle_len):
                break

            self.one_step_emulation(moons)

        return math.lcm(*cycle_len)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day12)
