import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution

C_VECTORS = {"forward": 1j, "down": 1, "up": -1}


class Solution(ISolution):
    def __init__(self, inp: Input):
        self.vectors = [C_VECTORS[action] * steps for action, steps in inp.get_lists("{{action}} {{steps|to_int}}")]

    def part_a(self):
        pos = sum(self.vectors)
        return int(pos.real * pos.imag)

    def part_b(self):
        pos = aim = 0
        for vector in self.vectors:
            if vector.real:
                aim += vector
            else:
                pos += vector + vector.imag * aim
        return int(pos.real * pos.imag)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
