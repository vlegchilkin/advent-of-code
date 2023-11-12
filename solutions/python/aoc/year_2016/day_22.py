import pytest
import numpy as np

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution, parse_with_template
from solutions.python.aoc.space import Spacer, C_BORDERS


class Year2016Day22(Solution):
    """2016/22: Grid Computing"""

    def __init__(self, inp: Input):
        text = "\n".join(inp.get_lines()[2:])
        ttp = (
            "/dev/grid/node-x{{x|to_int}}-y{{y|to_int}} "
            "{{size|to_int}}T {{used|to_int}}T {{avail|to_int}}T {{percent|to_int}}%"
        )
        data = parse_with_template(text, ttp)
        self.grid = Spacer.build({(d.y, d.x): (d.size, d.used, d.avail, d.percent) for d in data}).to_array()

    def part_a(self):
        count = 0
        for a, v_a in np.ndenumerate(self.grid):
            if not v_a[1]:
                continue
            for b, v_b in np.ndenumerate(self.grid):
                if a == b:
                    continue
                if v_a[1] <= v_b[2]:
                    count += 1
        return count

    def part_b(self):
        hole_pos, max_used = next(iter((complex(*d), v[2]) for d, v in np.ndenumerate(self.grid) if not v[3]))

        spacer = Spacer(self.grid.shape, directions=C_BORDERS)
        for pos, value in np.ndenumerate(self.grid):
            if value[1] <= max_used:
                spacer[complex(*pos)] = 1

        tr_corner = (spacer.m - 1) * 1j
        paths, end_pos = spacer.bfs(hole_pos, test=lambda p: p == tr_corner)
        assert tr_corner == end_pos, "path to the right corner doesn't exist"

        return paths[tr_corner][0] + 5 * (spacer.m - 2)  # shortest path to the corner plus 5 steps for every swap left


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day22)
