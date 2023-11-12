import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2016Day18(Solution):
    """2016/18: Like a Rogue"""

    def __init__(self, inp: Input):
        self.first_row = [v == "^" for v in inp.get_lines()[0]]

    def count_traps(self, rows):
        columns = len(self.first_row)
        buffer = [[False] + self.first_row + [False], [False] * (columns + 2)]
        traps = sum(buffer[0])
        for row in range(1, rows):
            line = row % 2
            for i in range(1, columns + 1):
                buffer[line][i] = buffer[1 - line][i - 1] != buffer[1 - line][i + 1]
            traps += sum(buffer[line])

        return rows * columns - traps

    def part_a(self):
        return self.count_traps(40)

    def part_b(self):
        return self.count_traps(400000)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day18)
