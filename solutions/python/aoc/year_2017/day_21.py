import collections

import pytest
import numpy as np
from numpy import int8

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2017Day21(Solution):
    """2017/21: Fractal Art"""

    def __init__(self, inp: Input):
        def _array(p):
            res = []
            for row in p.split("/"):
                res.append(list(map(lambda c: 1 if c == "#" else 0, row)))
            return res

        def parse(line):
            l, _, r = line.partition(" => ")
            return _array(l), _array(r)

        self.patterns = inp.get_lines(parse)
        self.start = _array(".#./..#/###")

    def run(self, steps):
        def shapes(a: list[list[int]]) -> set[bytes]:
            ar = np.array(a, dtype=int8)
            res = set()
            for flip in range(2):
                for rotate in range(4):
                    res.add(ar.tobytes())
                    ar = np.rot90(ar)
                ar = np.fliplr(ar)
            return res

        d = collections.defaultdict(dict)
        for f, t in self.patterns:
            _t = np.array(t)
            d[len(f)].update({shape: _t for shape in shapes(f)})

        buffer = np.array(self.start, dtype=int8)
        for _ in range(steps):
            dim = 3 if len(buffer) % 2 else 2
            to_dim = dim + 1
            n = len(buffer) // dim
            _buffer = np.ndarray(shape=(n * to_dim, n * to_dim), dtype=int8)
            for i in range(n):
                for j in range(n):
                    _buffer[i * to_dim : (i + 1) * to_dim, j * to_dim : (j + 1) * to_dim] = d[dim][
                        buffer[i * dim : (i + 1) * dim, j * dim : (j + 1) * dim].tobytes()
                    ]
            buffer = _buffer

        return np.sum(buffer)

    def part_a(self):
        return self.run(5)

    def part_b(self):
        return self.run(18)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day21)
