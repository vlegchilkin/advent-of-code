from solutions.python.aoc import Input, PuzzleData, Solution
from solutions.python.aoc.tpl import t_dist

TTP_TEMPLATE = """\
Sensor at x={{ sx | to_int }}, y={{ sy | to_int }}: closest beacon is at x={{ bx | to_int }}, y={{ by | to_int }}
"""


class Year2022Day15(Solution):
    def __init__(self, inp: Input, part_a_row):
        self.part_a_row = part_a_row
        self.data = [[(r.sx, r.sy), (r.bx, r.by)] for r in inp.get_objects(TTP_TEMPLATE)]
        self.sensors = [(d[0], t_dist(*d)) for d in self.data]

    def find_x_areas(self, y):
        areas = []
        for s in self.sensors:
            if (delta_x := s[1] - abs(s[0][1] - y)) >= 0:
                areas.append((s[0][0] - delta_x, s[0][0] + delta_x))
        return sorted(areas)

    def find_blind_zones(self, y) -> list[(int, int)]:
        areas = self.find_x_areas(y)
        max_x = areas[0][1]
        result = []
        for area in areas[1:]:
            if max_x < area[0]:
                result.append((max_x + 1, area[0] - 1))
            max_x = max(max_x, area[1])
        return result

    def part_a(self) -> int:
        x_areas = self.find_x_areas(self.part_a_row)
        part_a = x_areas[-1][1] - x_areas[0][0] + 1
        part_a -= len(set([d[1] for d in self.data if d[1][1] == self.part_a_row]))
        return part_a

    def part_b(self) -> int:
        for i in range(0, 4000000):
            if blind_zones := self.find_blind_zones(i):
                return blind_zones[0][0] * 4000000 + i


def test_simple():
    pd = PuzzleData("0")
    solution = Year2022Day15(pd.inp, 10)
    assert str(solution.part_a()) == pd.out.a
    assert str(solution.part_b()) == pd.out.b


def test_puzzle():
    pd = PuzzleData("puzzle")
    solution = Year2022Day15(pd.inp, 2000000)
    assert str(solution.part_a()) == pd.out.a
    assert str(solution.part_b()) == pd.out.b
