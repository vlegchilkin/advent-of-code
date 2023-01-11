import _md5

import pytest
import collections as cl

from aoc import Input, get_puzzles, PuzzleData, ISolution
from aoc.space import C_SIDES, Spacer


class Solution(ISolution):
    """2016/17: Two Steps Forward"""

    def __init__(self, inp: Input):
        self.passcode = inp.get_lines()[0]
        self.start = 0j
        self.finish = 3 + 3j

    def part_a_b(self):
        spacer = Spacer((4, 4))

        def get_possible():
            _h = _md5.md5(f"{self.passcode}{path}".encode("utf-8")).hexdigest()[:4]
            for index, (side, diff) in enumerate(C_SIDES.items()):
                if spacer.is_inside_ranges(_p := pos + diff) and _h[index] in "bcedf":
                    yield path + side, _p

        _min = _max = None
        q = cl.deque()
        q.append((self.start, ""))
        while q:
            pos, path = q.popleft()
            for _path, _pos in get_possible():
                if _pos == self.finish:
                    if _min is None:
                        _min = _path
                    _max = _path
                else:
                    q.append((_pos, _path))
        return _min, len(_max)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
