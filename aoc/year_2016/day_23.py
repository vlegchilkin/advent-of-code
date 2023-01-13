import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    """2016/23: Safe Cracking"""

    def __init__(self, inp: Input):
        self.instructions = [
            (cmd, args.split(" ")) for cmd, _, args in [line.partition(" ") for line in inp.get_lines()]
        ]

    def run(self, instructions, regs):
        def get_value(reg_or_int) -> int:
            return regs[reg_or_int] if reg_or_int in regs else int(reg_or_int)

        index = 0
        while 0 <= index < len(instructions):
            cmd, args = instructions[index]
            if index == 2:
                index = 10
                regs["a"] *= regs["b"]
                regs["b"] -= 1
                regs["c"] = regs["d"] = 0

            match cmd:
                case "inc":
                    if args[0] in regs:
                        regs[args[0]] += 1
                case "dec":
                    if args[0] in regs:
                        regs[args[0]] -= 1
                case "cpy":
                    if args[1] in regs:
                        regs[args[1]] = get_value(args[0])
                case "jnz":
                    if get_value(args[0]):
                        index += get_value(args[1]) - 1
                case "tgl":
                    value = get_value(args[0])
                    _index = index + value
                    if 0 <= _index < len(instructions):
                        _cmd, _args = instructions[_index]
                        if len(_args) == 1:
                            instructions[_index] = ("dec" if _cmd == "inc" else "inc", _args)
                        else:
                            instructions[_index] = ("cpy" if _cmd == "jnz" else "jnz", _args)

            index += 1

        return regs["a"]

    def part_a(self):
        return self.run(self.instructions.copy(), {"a": 7, "b": 0, "c": 0, "d": 0})

    def part_b(self):
        return self.run(self.instructions.copy(), {"a": 12, "b": 0, "c": 0, "d": 0})


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
