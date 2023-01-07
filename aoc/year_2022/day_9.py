import pytest

from aoc import Input, get_puzzles, PuzzleData
from aoc.space import C_SIDES


class Solution:
    def __init__(self, inp: Input):
        self.moves = [line.split(" ") for line in inp.get_lines()]

    @staticmethod
    def calc_move(head, tail):
        diff = head - tail
        abs_diff = abs(diff.real) + abs(diff.imag)

        if diff.real * diff.imag == 0 and abs_diff > 1:  # straight
            return diff / 2
        elif abs_diff > 2:  # diagonal
            return complex(-1 if diff.real < 0 else 1, -1 if diff.imag < 0 else 1)

    def count(self, chains):
        visited = set()
        rope = [0j for _ in range(chains)]
        visited.add(rope[-1])

        for direct, steps in self.moves:
            head_step = C_SIDES[direct]
            for _ in range(int(steps)):
                rope[0] += head_step
                for chain in range(1, chains):
                    if move := self.calc_move(rope[chain - 1], rope[chain]):
                        rope[chain] += move
                    else:
                        break
                visited.add(rope[-1])

        return len(visited)

    def part_a(self):
        return self.count(2)

    def part_b(self):
        return self.count(10)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
