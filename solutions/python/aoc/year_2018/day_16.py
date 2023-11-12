import re

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.tpl import t_replace

OP_FUNCTIONS = {
    "addr": lambda regs, a, b: regs[a] + regs[b],
    "addi": lambda regs, a, b: regs[a] + b,
    "mulr": lambda regs, a, b: regs[a] * regs[b],
    "muli": lambda regs, a, b: regs[a] * b,
    "banr": lambda regs, a, b: regs[a] & regs[b],
    "bani": lambda regs, a, b: regs[a] & b,
    "borr": lambda regs, a, b: regs[a] | regs[b],
    "bori": lambda regs, a, b: regs[a] | b,
    "setr": lambda regs, a, b: regs[a],
    "seti": lambda regs, a, b: a,
    "gtir": lambda regs, a, b: int(a > regs[b]),
    "gtri": lambda regs, a, b: int(regs[a] > b),
    "gtrr": lambda regs, a, b: int(regs[a] > regs[b]),
    "eqir": lambda regs, a, b: int(a == regs[b]),
    "eqri": lambda regs, a, b: int(regs[a] == b),
    "eqrr": lambda regs, a, b: int(regs[a] == regs[b]),
}


def execute(input_regs, op, a, b, c) -> tuple:
    return t_replace(input_regs, c, OP_FUNCTIONS[op](input_regs, a, b))


class Year2018Day16(Solution):
    """2018/16: Chronal Classification"""

    def __init__(self, inp: Input):
        it = inp.get_iter()

        def parse(block):
            return [tuple(map(int, re.findall(r"\d+", line))) for line in block]

        self.blocks = [parse(block) for block in inp.get_blocks(it)]
        next(it)
        self.program = [tuple(map(int, line.split(" "))) for line in it]

    def part_a_b(self):

        part_a = 0
        possible_codes = {op: set(range(len(OP_FUNCTIONS))) for op in iter(OP_FUNCTIONS)}
        for in_regs, (op_code, *args), out_regs in self.blocks:
            valid_operations = 0
            for op in OP_FUNCTIONS:
                if out_regs == execute(in_regs, op, *args):
                    valid_operations += 1
                elif op_code in possible_codes[op]:
                    possible_codes[op].remove(op_code)
            if valid_operations >= 3:
                part_a += 1

        op_codes = {}
        while possible_codes:
            for op, possible in list(possible_codes.items()):
                if len(possible) > 1:
                    continue
                op_codes[code := next(iter(possible))] = op
                del possible_codes[op]
                for values in possible_codes.values():
                    values.discard(code)

        regs = (0, 0, 0, 0)
        for op_code, *args in self.program:
            regs = execute(regs, op_codes[op_code], *args)
        part_b = regs[0]

        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day16)
