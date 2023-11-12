import itertools
import re

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2016Day21(Solution):
    """2016/21: Scrambled Letters and Hash"""

    def __init__(self, inp: Input):
        self.actions = inp.get_lines()
        self.password = "abcdefgh"

    def scrambler(self, password):
        def swap(pos_a, pos_b):
            buffer[pos_a], buffer[pos_b] = buffer[pos_b], buffer[pos_a]

        def rotate(steps):
            nonlocal buffer
            mid = steps % len(buffer)
            if mid > 0:
                mid = mid - len(buffer)
            buffer = buffer[-mid:] + buffer[:-mid]

        def reverse(pos_a, pos_b):
            nonlocal buffer
            buffer = buffer[:pos_a] + buffer[pos_a : pos_b + 1][::-1] + buffer[pos_b + 1 :]

        def move(pos_a, pos_b):
            nonlocal buffer
            value = buffer[pos_a]
            del buffer[pos_a]
            buffer.insert(pos_b, value)

        def parse_positions() -> (int, int):
            return tuple(map(int, re.findall(r"\d+", action)))

        buffer = list(password)
        for action in self.actions:
            if action.startswith("swap position"):
                swap(*parse_positions())
            elif action.startswith("reverse positions"):
                reverse(*parse_positions())
            elif action.startswith("move position"):
                move(*parse_positions())
            elif action.startswith("swap letter"):
                a, b = re.match(r"^swap letter (\w) with letter (\w)$", action).groups()
                swap(buffer.index(a), buffer.index(b))
            elif action.startswith("rotate based on position of letter"):
                x = buffer.index(action[-1])
                x += 2 if x >= 4 else 1
                rotate(x)
            elif action.startswith("rotate"):
                args = action.split(" ")
                rotate(int(args[2]) * (-1 if args[1] == "left" else 1))
            else:
                raise ValueError(f"Wrong action {action}")

        return "".join(buffer)

    def part_a(self):
        return self.scrambler(self.password)

    def part_b(self):
        for s in itertools.permutations(self.password):
            if self.scrambler(s) == "fbgdceah":
                return "".join(s)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day21)
