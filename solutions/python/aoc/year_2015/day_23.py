import re

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2015Day23(Solution):
    def __init__(self, inp: Input):
        r = re.compile(r"^(\w+) (.*)$")

        def parse(line):
            instr, attrs = r.match(line).groups()
            return instr, [c if c.islower() else int(c) for c in attrs.split(", ")]

        self.instructions = [parse(line) for line in inp.get_lines()]
        self.operators = {
            "hlf": lambda value: value // 2,
            "tpl": lambda value: value * 3,
            "inc": lambda value: value + 1,
        }
        self.jumps = {
            "jie": lambda value: value % 2 == 0,
            "jio": lambda value: value == 1,
            "jmp": lambda: True,
        }

    def simulate(self, regs):
        x = 0
        while 0 <= x < len(self.instructions):
            instr, attrs = self.instructions[x]
            if operator := self.operators.get(instr):
                regs[attrs[0]] = operator(regs[attrs[0]])
                x += 1
            elif jump := self.jumps.get(instr):
                if len(attrs) == 2:
                    need_jump = jump(regs[attrs[0]])
                else:
                    need_jump = jump()
                x += attrs[-1] if need_jump else 1
            else:
                raise ValueError(f"Illegal instruction {instr}")
        return regs

    def part_a(self):
        return self.simulate({"a": 0, "b": 0})["b"]

    def part_b(self):
        return self.simulate({"a": 1, "b": 0})["b"]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2015Day23)
