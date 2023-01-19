import copy
import re

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class BingoBoard:
    def __init__(self, lines):
        self.rows, self.columns = [5] * 5, [5] * 5
        self.values = {}
        for row, line in enumerate(lines):
            for col, value in enumerate(map(int, re.findall(r"\d+", line))):
                self.values[value] = (row, col)

    def mark(self, value):
        if (pos := self.values.get(value)) is None:
            return
        del self.values[value]
        self.rows[pos[0]] -= 1
        self.columns[pos[1]] -= 1
        return self.rows[pos[0]] * self.columns[pos[1]] == 0


class Year2021Day4(Solution):
    def __init__(self, inp: Input):
        inp_iter = inp.get_iter()
        self.numbers = list(map(int, next(inp_iter).split(",")))
        self.boards = []
        while next(inp_iter, None) is not None:
            lines = [next(inp_iter) for _ in range(5)]
            self.boards.append(BingoBoard(lines))

    def part_a(self):
        boards = copy.deepcopy(self.boards)
        for number in self.numbers:
            for board in boards:
                if board.mark(number):
                    return number * sum(board.values)

    def part_b(self):
        boards = copy.deepcopy(self.boards)
        for number in self.numbers:
            for board in list(boards):
                if board.mark(number):
                    if len(boards) == 1:
                        return number * sum(board.values)
                    boards.remove(board)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2021Day4)
