from operator import add, mul, gt, lt, eq
import dataclasses as dcs
import functools
from typing import Optional, Iterator

import pytest

from aoc import Input, get_puzzles, PuzzleData


@dcs.dataclass
class Packet:
    version: Optional[int] = None
    type_id: Optional[int] = None
    literal_value: Optional[int] = None
    operands: list["Packet"] = dcs.field(default_factory=lambda: [])

    @staticmethod
    def _parse(bin_iter: Iterator[str]) -> Optional["Packet"]:
        def bits(n) -> int:
            res = 0
            for i in range(n):
                res = (res << 1) + int(next(bin_iter))
            return res

        try:
            version = bits(3)
        except StopIteration:
            return None

        type_id = bits(3)
        if type_id == 4:  # literal
            value = 0
            while (x := bits(5)) & 0x10:
                value = (value << 4) + (x - 0x10)
            value = (value << 4) + x
            return Packet(version, type_id, literal_value=value)

        if bits(1):
            operands = [Packet._parse(bin_iter) for _ in range(bits(11))]
        else:  # total length
            sub_iter = (next(bin_iter) for _ in range(bits(15)))
            operands = []
            while op := Packet._parse(sub_iter):
                operands.append(op)
        return Packet(version, type_id, operands=operands)

    @staticmethod
    def parse_hex(hex_data: str) -> Optional["Packet"]:
        bin_data = bin(int(hex_data, 16))[2:].zfill(len(hex_data) * 4)
        return Packet._parse(iter(bin_data))


class Solution:
    def __init__(self, inp: Input):
        self.data = inp.get_lines()[0]

    def part_a(self):
        def versions(p: Packet) -> int:
            return p.version + sum(map(versions, p.operands))

        return versions(Packet.parse_hex(self.data))

    def part_b(self):
        operators = [add, mul, min, max, None, gt, lt, eq]

        def evaluate(p: Packet) -> int:
            if p.type_id == 4:
                return p.literal_value
            return functools.reduce(operators[p.type_id], map(evaluate, p.operands))

        return evaluate(Packet.parse_hex(self.data))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
