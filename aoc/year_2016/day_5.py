import hashlib
import itertools
from typing import Optional, Generator, Any

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    """2016/5: How About a Nice Game of Chess?"""

    def __init__(self, inp: Input):
        self.prefix = inp.get_text().strip()

    def _nice_md5_gen(self) -> Generator[str, None, None]:
        for index in itertools.count():
            if (v := hashlib.md5(f"{self.prefix}{index}".encode("utf-8")).hexdigest()).startswith("00000"):
                yield v

    def part_a_b(self) -> (Any, Any):
        part_a = ""
        part_b: list[Optional[str]] = [None] * 8

        for nice_md5 in self._nice_md5_gen():
            if len(part_a) < 8:
                part_a += nice_md5[5]
            if nice_md5[5].isdigit() and (pos := int(nice_md5[5])) < 8 and part_b[pos] is None:
                part_b[pos] = nice_md5[6]
                if None not in part_b:
                    break

        return part_a, "".join(part_b)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
