from typing import Callable, TypeVar

import pytest
from llist import dllist

from aoc import Input, get_puzzles, PuzzleData, Solution

T = TypeVar("T")


class Year2018Day14(Solution):
    """2018/14: Chocolate Charts"""

    def __init__(self, inp: Input):
        self.number = inp.get_lines(int)[0]

    @staticmethod
    def run(handler: Callable[[dllist], T]) -> T:
        recipes = dllist([3, 7])

        def append(recipe):
            recipes.append(recipe)
            return handler(recipes)

        p1, p2 = recipes.first, recipes.first.next
        for _ in range(200_000_000):  # infinite loop breaker
            total = p1.value + p2.value
            for v in [total // 10 or None, total % 10]:
                if v is not None and (res := append(v)) is not None:
                    return res

            for _ in range(p1.value + 1):
                p1 = p1.next or recipes.first

            for _ in range(p2.value + 1):
                p2 = p2.next or recipes.first

    def part_a(self):
        def handler(recipes: dllist):
            if len(recipes) >= self.number + 10:
                p = recipes.nodeat(self.number - 1)
                return "".join(map(str, [(p := p.next).value for _ in range(10)]))  # noqa: F841

        return self.run(handler)

    def part_b(self):
        pattern = list(map(int, str(self.number)))[::-1]

        def handler(recipes: dllist):
            pos = recipes.last
            for c in pattern:
                if pos.value != c:
                    break
                if (pos := pos.prev) is None:
                    return
            else:
                return len(recipes) - len(pattern)

        return self.run(handler)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day14)
