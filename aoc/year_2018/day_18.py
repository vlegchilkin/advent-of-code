from collections import Counter

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import Spacer


class Year2018Day18(Solution):
    """2018/18: Settlers of The North Pole"""

    def __init__(self, inp: Input):
        self.data = inp.get_array()

    def part_a_b(self):
        spacer = Spacer.build(self.data)

        def step():
            _at = {}
            for pos, v in spacer:
                links = Counter([spacer[link] for link in spacer.links(pos)])
                match v:
                    case ".":
                        _v = "|" if (links.get("|") or 0) >= 3 else v
                    case "|":
                        _v = "#" if (links.get("#") or 0) >= 3 else v
                    case "#":
                        _v = v if (links.get("#") or 0) >= 1 and (links.get("|") or 0) >= 1 else "."
                    case _:
                        raise ValueError(f"non-supported character: {v}")
                _at[pos] = _v
            spacer.at = _at

        def total():
            return sum(1 for c in spacer.at.values() if c == "|") * sum(1 for c in spacer.at.values() if c == "#")

        def _hash():
            return "".join([v for _, v in spacer])  # not so good, but the cycle is small enough, so no need to hash

        hashes, totals, last_step = {}, [], 1_000_000_000
        for t in range(last_step):
            if (_h := _hash()) in hashes:
                t0 = hashes[_h]
                last_step = ((last_step - t) % (t - t0)) + t0
                break
            totals.append(total())
            hashes[_h] = t
            step()

        return totals[10], totals[last_step]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day18)
