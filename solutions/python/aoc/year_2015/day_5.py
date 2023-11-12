import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2015Day5(Solution):
    def __init__(self, inp: Input):
        self.lines = inp.get_lines()

    def part_a(self):
        def nice(line):
            for s in ["ab", "cd", "pq", "xy"]:
                if s in line:
                    return False

            if sum([c in "aeiou" for c in line]) < 3:
                return False

            twice_count = sum([line[i] == line[i - 1] for i in range(1, len(line))])
            return twice_count > 0

        return sum([nice(line) for line in self.lines])

    def part_b(self):
        def nice(line):
            for i in range(0, len(line) - 2):
                if line[i] == line[i + 2]:
                    break
            else:
                return False

            for i in range(0, len(line) - 2):
                for j in range(i + 2, len(line)):
                    if line[i : i + 2] == line[j : j + 2]:
                        return True

            return False

        return sum([nice(line) for line in self.lines])


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2015Day5)
