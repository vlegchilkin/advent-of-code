import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2017Day17(Solution):
    """2017/17: Spinlock"""

    def __init__(self, inp: Input):
        self.steps = inp.get_lines(int)[0]

    def part_a(self):
        buffer = [0]
        pos = 0
        for value in range(1, 2018):
            pos = (pos + self.steps) % len(buffer) + 1
            buffer.insert(pos, value)
        return buffer[pos + 1]

    def part_b(self):
        pos, second_pos = 0, None
        for value in range(1, 50_000_001):
            pos = (pos + self.steps) % value + 1
            if pos == 1:
                second_pos = value
        return second_pos


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day17)
