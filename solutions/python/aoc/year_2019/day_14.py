import collections as cl

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.math import ceil_div


class Year2019Day14(Solution):
    """2019/14: Space Stoichiometry"""

    def __init__(self, inp: Input):
        records = inp.get_lists('{{ src | ORPHRASE | to_str_list(sep=", ")}} =&gt; {{dst | ORPHRASE}}')

        def parse(s: str) -> tuple[int, str]:
            cntr, name = s.split(" ")
            return int(cntr), name

        self.records = dict()
        for src, dst in records:
            cnt, material = parse(dst)
            self.records[material] = (cnt, [parse(v) for v in src])

    def _count_required_ore(self, fuel: int) -> int:
        warehouse = cl.defaultdict(int)

        def produce(cnt, material):
            if material == "ORE":
                return cnt

            remains = cnt - warehouse[material]
            if remains <= 0:
                warehouse[material] = -remains
                return 0

            recept_cnt, recept_ingredients = self.records[material]
            factor = ceil_div(remains, recept_cnt)

            ore_used = 0
            for ing_cnt, ing_material in recept_ingredients:
                ore_used += produce(ing_cnt * factor, ing_material)

            warehouse[material] = factor * recept_cnt - remains
            return ore_used

        return produce(fuel, "FUEL")

    def part_a(self):
        return self._count_required_ore(1)

    def part_b(self):
        lo = 1
        hi = ore_limit = 1_000_000_000_000
        while lo < hi:
            mid = (lo + hi) // 2
            ore_required = self._count_required_ore(mid)
            if ore_required < ore_limit:
                lo = mid + 1
            else:
                hi = mid
        return lo - 1


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day14)
