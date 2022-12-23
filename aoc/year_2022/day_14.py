import pytest

from aoc import Input, Spacer, D, get_puzzles, PuzzleData

DIRECTIONS = [D.SOUTH, D.SOUTH_WEST, D.SOUTH_EAST]


class Solution:
    def __init__(self, inp: Input):
        lines = inp.get_lines()
        self.spacer = Spacer(1000, 1000, default_directions=DIRECTIONS)
        self.a = self.spacer.new_array(0)
        max_row = 0
        for line in lines:
            points = [[int(x) for x in reversed(step.split(","))] for step in line.split(" -> ")]
            for i in range(1, len(points)):
                s, t = sorted([points[i - 1], points[i]])
                self.a[s[0] : t[0] + 1, s[1] : t[1] + 1] = 1
                max_row = max(max_row, t[0])

        self.floor = max_row + 2
        self.a[self.floor, :] = 1

    def drop(self, pos, row_limit):
        if self.a[pos]:
            return False

        while next_pos := next(self.spacer.get_links(pos, test=lambda p: not self.a[p] and p[0] <= row_limit), None):
            pos = next_pos

        if pos[0] < row_limit:
            self.a[pos] = 2
            return True

    def part_a_b(self) -> (int, int):
        source = (0, 500)
        count = 0
        while self.drop(source, self.floor - 2):
            count += 1
        part_a = count

        while self.drop(source, self.floor):
            count += 1
        return part_a, count


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
