import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution


class Solution(ISolution):
    def __init__(self, inp: Input):
        self.line = inp.get_lines()[0]

    @staticmethod
    def look_and_say(line: str) -> str:
        result = ""
        digit, count = None, 0

        for c in line:
            if c == digit:
                count += 1
                continue
            if count:
                result += f"{count}{digit}"
            digit, count = c, 1

        if count:
            result += f"{count}{digit}"

        return result

    def simulate(self, times) -> str:
        line = self.line
        for _ in range(times):
            line = self.look_and_say(line)
        return line

    def part_a(self):
        return len(self.simulate(40))

    def part_b(self):
        return len(self.simulate(50))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
