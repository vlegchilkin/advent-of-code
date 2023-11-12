import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2017Day11(Solution):
    """2017/11: Hex Ed"""

    def __init__(self, inp: Input):
        self.moves = inp.get_lines(lambda line: line.split(","))[0]

    def part_a_b(self):
        steps = {"nw": 0 - 1j, "n": -1 + 0j, "ne": 0 + 1j, "sw": 1 - 1j, "s": 1 + 0j, "se": 1 + 1j}

        def dist():
            x = abs(pos.imag)
            if pos.real < 0:
                y = abs(pos.real) - (x - x // 2)
            else:
                y = pos.real - x // 2
            return int(x + max(y, 0))

        pos, _max_dist = 0j, 0
        for move in self.moves:
            even_diagonal_offset = len(move) == 2 and (pos.imag % 2) == 0
            pos += steps[move] - even_diagonal_offset
            _max_dist = max(_max_dist, dist())

        return dist(), _max_dist


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day11)
