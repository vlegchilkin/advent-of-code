import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2015Day17(Solution):
    def __init__(self, inp: Input):
        self.containers = inp.get_lines(int)

    def fill(self, container_id, volume, limit):
        if container_id < 0:
            return not volume

        counter = self.fill(container_id - 1, volume, limit)
        if self.containers[container_id] <= volume and limit:
            counter += self.fill(container_id - 1, volume - self.containers[container_id], limit - 1)

        return counter

    def part_a(self):
        return self.fill(len(self.containers) - 1, 150, len(self.containers))

    def part_b(self):
        minimal = 1
        while not (result := self.fill(len(self.containers) - 1, 150, minimal)):
            minimal += 1
        return result


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2015Day17)
