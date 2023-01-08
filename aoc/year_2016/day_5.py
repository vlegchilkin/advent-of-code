import hashlib
import itertools
from typing import Optional, Generator

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    """Year 2016 / Day 5: How About a Nice Game of Chess?"""

    def __init__(self, inp: Input):
        self.prefix = inp.get_text().strip()

    def _nice_md5_gen(self) -> Generator[str, None, None]:
        for index in itertools.count():
            if (v := hashlib.md5(f"{self.prefix}{index}".encode("utf-8")).hexdigest()).startswith("00000"):
                yield v

    def part_a(self):
        return "".join(v[5] for v in itertools.islice(self._nice_md5_gen(), 8))

    def part_b(self):
        password: list[Optional[str]] = [None] * 8
        for nice_md5 in self._nice_md5_gen():
            if nice_md5[5].isdigit() and (pos := int(nice_md5[5])) < 8 and password[pos] is None:
                password[pos] = nice_md5[6]
                if None not in password:
                    break

        return "".join(password)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
