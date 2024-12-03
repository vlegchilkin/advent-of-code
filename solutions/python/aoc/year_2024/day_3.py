import re
import itertools as it
import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution

INSTRUCTIONS_REG = re.compile(r"don't\(\)|do\(\)|mul\(-?\d+,-?\d+\)")


def compute(instructions: list[str]) -> int:
    active = True
    result = 0
    for instr in instructions:
        if instr == "do()":
            active = True
        elif instr == "don't()":
            active = False
        elif not active:
            continue

        if instr.startswith("mul("):
            a, b = map(int, re.findall(r"-?\d+", instr))
            result += a * b

    return result


class Year2024Day3(Solution):
    """2024/3: Mull It Over"""

    def __init__(self, inp: Input):
        lines = inp.get_lines(lambda x: INSTRUCTIONS_REG.findall(x))
        self.instructions = list(it.chain(*lines))

    def part_a(self):
        mul_instr = [instr for instr in self.instructions if instr.startswith("mul(")]
        return compute(mul_instr)

    def part_b(self):
        return compute(self.instructions)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2024Day3)
