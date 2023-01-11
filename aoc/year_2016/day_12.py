import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    """2016/12: Leonardo's Monorail"""

    def __init__(self, inp: Input):
        self.instructions = [
            (cmd, args.split(" ")) for cmd, _, args in [line.partition(" ") for line in inp.get_lines()]
        ]

    def run(self, regs):
        def get_value(reg_or_int) -> int:
            return regs[reg_or_int] if reg_or_int in regs else int(reg_or_int)

        index = 0
        while 0 <= index < len(self.instructions):
            cmd, args = self.instructions[index]
            match cmd:
                case "inc":
                    regs[args[0]] += 1
                case "dec":
                    regs[args[0]] -= 1
                case "cpy":
                    regs[args[1]] = get_value(args[0])
                case "jnz":
                    if get_value(args[0]):
                        index += int(args[1]) - 1
            index += 1

        return regs["a"]

    def part_a(self):
        return self.run({r: 0 for r in "abcd"})

    def part_b(self):
        return self.run({"a": 0, "b": 0, "c": 1, "d": 0})


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
