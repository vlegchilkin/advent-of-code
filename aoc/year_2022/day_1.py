import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2022Day1(Solution):
    def __init__(self, inp: Input):
        sums, capacities = 0, []
        for line in inp.get_lines():
            if line:
                sums += int(line)
            else:
                capacities.append(sums)
                sums = 0
        capacities.append(sums)
        self.top3 = sorted(capacities, reverse=True)[:3]

    def part_a(self):
        return self.top3[0]

    def part_b(self):
        return sum(self.top3)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2022Day1)
