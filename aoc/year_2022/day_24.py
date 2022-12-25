import pytest
import numpy as np
from aoc import Input, get_puzzles, PuzzleData, D, Spacer, D_BORDERS, t_sum, D_MOVES


class Solution:
    def __init__(self, inp: Input):
        data = inp.get_array()

        if len(enter_columns := [j for j, v in enumerate(data[0, :]) if v == "."]) == 1:
            self.start = -1, enter_columns[0] - 1
        else:
            raise ValueError("Wrong enter configuration (multiple or none)")

        if len(exit_columns := [j for j, v in enumerate(data[-1, :]) if v == "."]) == 1:
            self.finish = data.shape[0] - 2, exit_columns[0] - 1
        else:
            raise ValueError("Wrong exit configuration (multiple or none)")

        self.blizzards = {d: set() for d in D_MOVES.values()}
        maze = data[1:-1, 1:-1]
        for pos, c in np.ndenumerate(maze):
            if c in D_MOVES:
                self.blizzards[D_MOVES[c]].add(pos)
        self.spacer = Spacer(*maze.shape, default_directions=D_BORDERS)

    def blizzards_step(self, blizzards):
        for d in list(blizzards.keys()):
            updated = set()
            for v in blizzards[d]:
                updated.add(self.spacer.move(v, d))
            blizzards[d] = updated

    def your_step(self, blizzards, positions):
        blocked_positions = set()
        for d in blizzards.values():
            blocked_positions |= d

        for pos in list(positions):
            links = set(self.spacer.get_links(pos, test=lambda x: x not in blocked_positions))
            positions |= links

        positions -= blocked_positions

    def trip(self, blizzards, straight=True):
        positions = {self.start if straight else self.finish}
        doorway = t_sum(self.finish, (-1, 0)) if straight else t_sum(self.start, (1, 0))
        time = 0

        def step():
            self.blizzards_step(blizzards)
            self.your_step(blizzards, positions)
            nonlocal time
            time += 1

        while doorway not in positions:
            step()
        step()  # step outside the maze from doorway to finish
        return time

    def part_a(self):
        return self.trip(self.blizzards.copy())

    def part_b(self):
        blizzards = self.blizzards.copy()
        return self.trip(blizzards) + self.trip(blizzards, straight=False) + self.trip(blizzards)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
