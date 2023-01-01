import itertools

import pytest

from aoc import Input, get_puzzles, PuzzleData

NUMBERS = ["abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]
SEGMENTS = NUMBERS[8]


class Solution:
    def __init__(self, inp: Input):
        def parse(line):
            return [item.split(" ") for item in line.split(" | ")]

        self.cases = inp.get_lines(parse)

    def part_a(self):
        return sum([len([i for i in item[1] if len(i) in [2, 3, 4, 7]]) for item in self.cases])

    @staticmethod
    def bruteforce(inp, out) -> int:
        def encode(num, codec):
            return tuple(sorted((codec[ord(ch) - 97] for ch in NUMBERS[num])))

        def decode(value, codec) -> int:
            pattern = tuple(sorted(value))
            for i in range(10):
                if encode(i, codec) == pattern:
                    return i

        inp_set = {tuple(sorted(i)) for i in inp}
        for c in itertools.permutations(SEGMENTS):
            if inp_set == {encode(i, c) for i in range(10)}:
                return int("".join([str(decode(o, c)) for o in out]))

    def part_b(self):
        return sum((self.bruteforce(inp, out) for inp, out in self.cases))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
