import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        pass

    def part_a(self):
        return None

    def part_b(self):
        return None


if __name__ == "__main__":  # Playground here
    solution = Solution(Input(0))
    assert solution.part_a() is None
    assert solution.part_b() is None


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
