from enum import IntEnum
import dataclasses as dc

import pytest
import itertools as it
from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import Spacer
from aoc.year_2019 import IntcodeComputer


class TileType(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


@dc.dataclass
class Tile:
    x: int
    y: int
    type: TileType

    @staticmethod
    def parse(output) -> list['Tile']:
        return list(Tile(*tile) for tile in it.batched(output, 3))

class Board:
    def __init__(self):
        self.spacer = Spacer(ranges=None)
        self.blocks: int = None
        self.score: int = None
        self.ball: complex = None
        self.paddle: complex = None

    def update(self, items: list[Tile]):
        for tile in items:
            if tile.x >= 0:
                self.spacer[tile.y + tile.x * 1j] = tile.type
            else:
                self.score = tile.type

        blocks = 0
        for pos, value in self.spacer:
            match value:
                case TileType.BALL:
                    self.ball = pos
                case TileType.PADDLE:
                    self.paddle = pos
                case TileType.BLOCK:
                    blocks += 1
        self.blocks = blocks

    def __str__(self):
        return str(self.spacer)


class Year2019Day13(Solution):
    """2019/13: Care Package"""

    def __init__(self, inp: Input):
        self.instructions = list(map(int, inp.get_text().split(",")))

    def part_a(self):
        computer = IntcodeComputer(self.instructions)
        output = computer.run()
        items = Tile.parse(output)
        number_of_blocks = sum(tile.type == TileType.BLOCK for tile in items)
        return number_of_blocks

    def part_b(self):
        computer = IntcodeComputer(self.instructions)
        computer.memory[0] = 2
        output = computer.run()
        items = Tile.parse(output)

        board = Board()
        board.update(items)

        print(board)
        while board.blocks != 0:
            diff = board.ball.imag - board.paddle.imag
            joystick_command = [-1 if diff < 0 else 1 if diff > 0 else 0]
            output = computer.run(joystick_command)
            items = Tile.parse(output)
            board.update(items)

        return board.score


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day13)
