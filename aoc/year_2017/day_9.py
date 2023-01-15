import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Year2017Day9(ISolution):
    """2017/9: Stream Processing"""

    def __init__(self, inp: Input):
        self.stream = inp.get_lines()[0]

    def part_a_b(self):
        garbage = ignore_next = False
        depth = part_a = part_b = 0

        for c in self.stream:
            if garbage:
                if ignore_next:
                    ignore_next = False
                elif c == "!":
                    ignore_next = True
                elif c == ">":
                    garbage = False
                else:
                    part_b += 1
            else:
                if c == "{":
                    depth += 1
                elif c == "}":
                    part_a += depth
                    depth -= 1
                elif c == "<":
                    garbage = True

        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day9)
