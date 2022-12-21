from itertools import cycle
from typing import Optional

from aoc import Input


class Simulation:
    def __init__(self, rocks, moves):
        self.glass = []
        self._move_iter = iter(cycle(moves))
        self._rock_iter = iter(cycle(rocks))

    def _is_intersect(self, rock, pos):
        if pos[1] < 0 or pos[1] + len(rock[0]) > 7:
            return True

        for i, r in enumerate(rock):
            if (x := pos[0] + i) >= len(self.glass):
                continue
            for j, v in enumerate(r):
                if self.glass[x][pos[1] + j] + rock[i][j] > 1:
                    return True

        return False

    def _drop(self, rock, pos) -> (int, int):
        new_pos = pos
        shifted = (pos[0], pos[1] + next(self._move_iter))
        if not self._is_intersect(rock, shifted):
            new_pos = shifted
        if new_pos[0] > 0:
            dropped = (new_pos[0] - 1, new_pos[1])
            if not self._is_intersect(rock, dropped):
                new_pos = dropped

        if new_pos[0] != pos[0] and new_pos[0] >= 0:
            return self._drop(rock, new_pos)
        return new_pos

    def run(self, count=1):
        for _ in range(count):
            rock = next(self._rock_iter)
            pos = self._drop(rock, (len(self.glass) + 3, 2))
            while len(self.glass) < pos[0] + len(rock):
                self.glass.append([0] * 7)
            for i, r in enumerate(rock):
                for j, v in enumerate(r):
                    self.glass[pos[0] + i][pos[1] + j] += rock[i][j]

        return len(self.glass)


class Solution:
    def __init__(self, inp: Input):
        blocks = Input(0).get_blocks()
        self.rocks = [[[1 if c == "#" else 0 for c in line] for line in reversed(block)] for block in blocks]
        self.moves = [1 if c == ">" else -1 for c in inp.get_text().strip()]

    def _build_sim(self):
        return Simulation(self.rocks, self.moves)

    def part_a(self):
        return self._build_sim().run(2022)

    @staticmethod
    def _find_cycle(d) -> Optional[tuple[int, int]]:
        """
        Finds a four times repeated sequence (X) at the end of deltas list [_XXXX]
        :return a sequence's length and a total height of the sequence.
        """
        if len(d) < 10:
            return
        for size in range(len(d) // 6, len(d) // 5):
            for i in range(size):
                if not (d[-1 * size - i] == d[-2 * size - i] == d[-3 * size - i] == d[-4 * size - i]):
                    break
            else:
                return size, sum(d[-size:])

    def part_b(self):
        iterations = 1000000000000
        simulation = self._build_sim()

        top_height, deltas = 0, []
        while not (loop := self._find_cycle(deltas)) and len(deltas) < iterations:
            new_height = simulation.run()
            deltas.append(new_height - top_height)
            top_height = new_height

        if remains := iterations - len(deltas):
            return (remains // loop[0]) * loop[1] + simulation.run(remains % loop[0])
        else:
            return top_height


def test_simple():
    solution = Solution(Input(1))
    assert solution.part_a() == 3068
    assert solution.part_b() == 1514285714288


def test_puzzle():
    solution = Solution(Input())
    assert solution.part_a() == 3239
    assert solution.part_b() == 1594842406882
