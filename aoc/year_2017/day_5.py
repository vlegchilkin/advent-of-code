import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2017Day5(Solution):
    """2017/5: A Maze of Twisty Trampolines, All Alike"""

    def __init__(self, inp: Input):
        self.jumps = inp.get_lines(int)

    def run(self, func):
        jumps = self.jumps.copy()
        index = count = 0
        while 0 <= index < len(jumps):
            count += 1
            value = jumps[index]
            jumps[index] += func(value)
            index += value
        return count

    def part_a(self):
        return self.run(lambda value: 1)

    def part_b(self):
        return self.run(lambda value: 1 if value < 3 else -1)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day5)
