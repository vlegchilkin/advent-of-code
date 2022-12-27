import pytest

from aoc import Input, get_puzzles, PuzzleData, Spacer, IT


class Solution:
    def __init__(self, inp: Input):
        inp_arr = inp.get_array(lambda c: c == "#")
        self.spacer = Spacer(*inp_arr.shape)
        self.on_lamps = Spacer.filter(inp_arr)

    def switch(self, on_lamps) -> set:
        result = set()
        for pos in self.spacer.iter():
            on_neighbours = sum(1 for _ in self.spacer.get_links(pos, test=lambda p: p in on_lamps))
            if on_neighbours == 3 or (on_neighbours == 2 and pos in on_lamps):
                result.add(pos)
        return result

    def part_a(self):
        on_lamps = self.on_lamps.copy()
        for _ in range(100):
            on_lamps = self.switch(on_lamps)
        return len(on_lamps)

    def part_b(self):
        corners = set(self.spacer.iter(it=IT.CORNERS))
        lamps = self.on_lamps.copy() | corners
        for _ in range(100):
            lamps = self.switch(lamps) | corners
        return len(lamps)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
