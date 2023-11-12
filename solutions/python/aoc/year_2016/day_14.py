import _md5

import pytest
import collections as cl

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2016Day14(Solution):
    """2016/14: One-Time Pad"""

    def __init__(self, inp: Input):
        self.salt = inp.get_lines()[0]

    def gen(self, cycles):
        def _gen_hash():
            index = 0
            while True:
                index += 1
                _hash = _md5.md5(f"{self.salt}{index}".encode("utf-8")).hexdigest()
                for _ in range(cycles):
                    _hash = _md5.md5(_hash.encode("utf-8")).hexdigest()
                yield _hash

        buffer = cl.deque()
        count = 0
        it = _gen_hash()
        while True:
            while len(buffer) < 1001:
                buffer.append(next(it))
            count += 1
            h = buffer.popleft()
            for i in range(0, len(h) - 2):
                if h[i] == h[i + 1] == h[i + 2]:
                    five = h[i] * 5
                    if any(_h for _h in buffer if five in _h):
                        yield count
                    break

    def get_otp(self, cycles=0):
        it = self.gen(cycles)
        return [next(it) for _ in range(64)]

    def part_a(self):
        return self.get_otp()[-1]

    def part_b(self):
        return self.get_otp(2016)[-1]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day14)
