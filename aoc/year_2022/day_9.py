import pytest

from aoc import Input, D, get_test_cases, TestCase

DIRECTIONS = {"U": D.NORTH, "D": D.SOUTH, "R": D.EAST, "L": D.WEST}


class Solution:
    def __init__(self, inp: Input):
        self.moves = [line.split(" ") for line in inp.get_lines()]

    @staticmethod
    def calc_move(head, tail):
        diff = head[0] - tail[0], head[1] - tail[1]
        abs_diff = abs(diff[0]) + abs(diff[1])

        if diff[0] * diff[1] == 0 and abs_diff > 1:  # straight
            return (diff[0] // 2), (diff[1] // 2)
        elif abs_diff > 2:  # diagonal
            return -1 if diff[0] < 0 else 1, -1 if diff[1] < 0 else 1

    def count(self, chains):
        visited = set()
        rope = [(0, 0) for _ in range(chains)]
        visited.add(rope[-1])

        for direct, steps in self.moves:
            head_step = DIRECTIONS[direct]
            for _ in range(int(steps)):
                rope[0] = rope[0][0] + head_step[0], rope[0][1] + head_step[1]
                for chain in range(1, chains):
                    if move := self.calc_move(rope[chain - 1], rope[chain]):
                        rope[chain] = rope[chain][0] + move[0], rope[chain][1] + move[1]
                    else:
                        break
                visited.add(rope[-1])

        return len(visited)

    def part_a(self):
        return self.count(2)

    def part_b(self):
        return self.count(10)


@pytest.mark.parametrize("tc", get_test_cases(), ids=str)
def test_case(tc: TestCase):
    tc.assertion(Solution)
