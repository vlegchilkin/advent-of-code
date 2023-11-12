import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2022Day10(Solution):
    def __init__(self, inp: Input):
        input_lines = inp.get_lines()

        self.timeline = [1]
        for line in input_lines:
            self.timeline.append(self.timeline[-1])
            if line != "noop":
                self.timeline.append(self.timeline[-1] + (int(line.split(" ")[1])))

    def part_a(self):
        cycles = [20 + i * 40 for i in range(6)]
        part_a = sum([self.timeline[c - 1] * c for c in cycles])
        return part_a

    def part_b(self):
        crt = [[], [], [], [], [], []]
        for i in range(40 * 6):
            pixel = "#" if i % 40 in (self.timeline[i] - 1, self.timeline[i], self.timeline[i] + 1) else "."
            crt[i // 40].append(pixel)
        return "\n".join([" ".join(line) for line in crt]) + "\n"


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2022Day10)
