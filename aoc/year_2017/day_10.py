import functools
import math
import operator
import re

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Year2017Day10(ISolution):
    """2017/10: Knot Hash"""

    def __init__(self, inp: Input):
        self.line = inp.get_lines()[0]

    @staticmethod
    def sparse_hash(lengths, rounds):
        buffer = [i for i in range(256)]
        index = skip = 0
        for r in range(rounds):
            for length in lengths:
                _a = min(length, len(buffer) - index)
                _reversed = (buffer[index : index + _a] + buffer[: length - _a])[::-1]
                for c in _reversed:
                    buffer[index] = c
                    index = (index + 1) % len(buffer)
                index = (index + skip) % len(buffer)
                skip += 1
        return buffer

    @staticmethod
    def dense_hash(buffer) -> str:
        _hash = [functools.reduce(operator.xor, buffer[i * 16 : (i + 1) * 16]) for i in range(16)]
        return bytes(_hash).hex()

    def part_a(self):
        lengths = list(map(int, re.findall(r"\d+", self.line)))
        return math.prod(self.sparse_hash(lengths, 1)[:2])

    def part_b(self):
        lengths = list(self.line.encode("utf-8")) + [17, 31, 73, 47, 23]
        _sparse_hash = self.sparse_hash(lengths, 64)
        return self.dense_hash(_sparse_hash)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day10)
