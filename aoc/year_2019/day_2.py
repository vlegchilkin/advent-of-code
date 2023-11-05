import operator

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2019Day2(Solution):
    """2019/2: 1202 Program Alarm"""

    def __init__(self, inp: Input):
        self.instructions = list(map(int, inp.get_text().split(",")))

    def run(self, noun, verb):
        buffer = self.instructions.copy()
        buffer[1], buffer[2] = noun, verb
        for pos in range(0, len(buffer), 4):
            match buffer[pos]:
                case 1:
                    op = operator.add
                case 2:
                    op = operator.mul
                case 99:
                    break
                case _:
                    raise ValueError()
            buffer[buffer[pos + 3]] = op(buffer[buffer[pos + 1]], buffer[buffer[pos + 2]])
        return buffer[0]

    def part_a(self):
        return self.run(12, 2)

    def part_b(self):
        required = 19690720
        for noun in range(100):
            for verb in range(100):
                if self.run(noun, verb) == required:
                    return noun * 100 + verb


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day2)
