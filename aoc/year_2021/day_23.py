import pytest
from numpy import Inf

from aoc import Input, get_puzzles, PuzzleData
from aoc.tpl import t_add_pos, t_pop_left, t_push_left


class Solution:
    def __init__(self, inp: Input):
        self.ar = inp.get_array()

    @staticmethod
    def _find_shortest(parking, final_parking):
        def do_park(park, row_id):
            return tuple(pl if idx != row_id - 1 else t_push_left(pl, row_id) for idx, pl in enumerate(park))

        def do_unpark(park, row_id):
            return tuple(pl if idx != row_id - 1 else t_pop_left(pl) for idx, pl in enumerate(park))

        def path_to_exit(park):
            for i, v in enumerate(park):
                if v:
                    return i, v
            return len(park), None

        def recu(hall, park) -> int:
            if (cached := shortest.get((hall, park))) is not None:
                return cached
            shortest[(hall, park)] = best = Inf

            # 1.from hall to park
            for pos, r_id in enumerate(hall):
                if r_id and all(p in [0, r_id] for p in park[r_id - 1]):  # row r_id is ready to park
                    if (pos <= r_id and sum(hall[pos + 1 : r_id + 1])) or (pos > r_id and sum(hall[r_id + 1 : pos])):
                        continue  # no clean path via hall to row with r_id
                    path = row_to_hall_paths[r_id - 1][pos] + path_to_exit(park[r_id - 1])[0]
                    cost = path * (10 ** (r_id - 1))
                    best = min(best, cost + recu(t_add_pos(hall, pos, -r_id), do_park(park, r_id)))

            # 2.from park to hall
            for r_id, row in enumerate(park, start=1):
                if any(c not in [0, r_id] for c in row):
                    exit_path, top_item = path_to_exit(row)
                    for hall_way in [range(r_id, -1, -1), range(r_id + 1, len(hall))]:
                        for hall_pos in hall_way:
                            if hall[hall_pos]:
                                break
                            cost = (1 + exit_path + row_to_hall_paths[r_id - 1][hall_pos]) * (10 ** (top_item - 1))
                            best = min(best, cost + recu(t_add_pos(hall, hall_pos, top_item), do_unpark(park, r_id)))

            shortest[(hall, park)] = best
            return best

        empty_hall = (0, 0, 0, 0, 0, 0, 0)
        row_to_hall_paths = [[2, 1, 1, 3, 5, 7, 8], [4, 3, 1, 1, 3, 5, 6], [6, 5, 3, 1, 1, 3, 4], [8, 7, 5, 3, 1, 1, 2]]
        shortest = {(empty_hall, final_parking): 0}

        return recu(empty_hall, parking)

    def _solve(self, data):
        n = len(data) - 3
        parking = tuple(tuple(ord(data[i][3 + j * 2]) - 0x40 for i in range(2, 2 + n)) for j in range(0, 4))
        final_parking = tuple(tuple(j + 1 for _ in range(2, 2 + n)) for j in range(0, 4))
        return self._find_shortest(parking, final_parking)

    def part_a(self):
        return self._solve(self.ar)

    def part_b(self):
        data = self.ar.tolist()
        data = data[:3] + [list("  #D#C#B#A#  "), list("  #D#B#A#C#  ")] + data[3:]
        return self._solve(data)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
