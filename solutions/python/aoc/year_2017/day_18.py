import collections
from typing import Optional

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2017Day18(Solution):
    """2017/18: Duet"""

    def __init__(self, inp: Input):
        self.instructions = [
            (cmd, args.split(" ")) for cmd, _, args in [line.partition(" ") for line in inp.get_lines()]
        ]

    def run(
        self, regs, index=0, inp: Optional[collections.deque] = None, interceptor=None
    ) -> (dict, int, collections.deque):
        def get_value(reg_or_int) -> int:
            return regs[reg_or_int] if reg_or_int in regs else int(reg_or_int)

        snd_buffer = collections.deque()
        while 0 <= index < len(self.instructions):
            cmd, args = self.instructions[index]
            if interceptor and (_index := interceptor(index, cmd, args)):
                index = _index
                continue

            match cmd:
                case "snd":
                    snd_buffer.append(get_value(args[0]))
                case "set":
                    regs[args[0]] = get_value(args[1])
                case "add":
                    regs[args[0]] += get_value(args[1])
                case "sub":
                    regs[args[0]] -= get_value(args[1])
                case "mul":
                    regs[args[0]] *= get_value(args[1])
                case "mod":
                    regs[args[0]] %= get_value(args[1])
                case "rcv":
                    if inp:
                        value = inp.popleft()
                        regs[args[0]] = value
                    else:
                        return regs, index, snd_buffer
                case "jgz":
                    if get_value(args[0]) > 0:
                        index += get_value(args[1]) - 1
                case "jnz":
                    if get_value(args[0]):
                        index += get_value(args[1]) - 1
            index += 1

    def part_a(self):
        regs = collections.defaultdict(int)
        _, _, buffer = self.run(regs)
        return buffer[-1]

    def part_b(self):
        states = [(collections.defaultdict(int, p=_id), 0) for _id in [0, 1]]
        result = 0
        snd_buffer: Optional[collections.deque] = None
        while snd_buffer is None or len(snd_buffer) > 0:
            for p in [0, 1]:
                *states[p], snd_buffer = self.run(*states[p], inp=snd_buffer)
            result += len(snd_buffer)

        return result


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day18)
