import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
import numpy as np
import math
import collections as cl
from heapq import heappush, heappop
import itertools as it


class Year2019Day10(Solution):
    """2019/10: Monitoring Station"""

    def __init__(self, inp: Input):
        self.map = inp.get_array()

    def find_monitoring_station(self):
        def vector(src, dst):
            dx, dy = dst[0] - src[0], dst[1] - src[1]
            gcd = abs(math.gcd(dx, dy))
            return (dx // gcd, dy // gcd), dx * dx + dy * dy

        def vectorize():
            _vectors = cl.defaultdict(list)
            for aim_pos, aim_char in np.ndenumerate(self.map):
                if aim_char == '.' or aim_pos == pos:
                    continue
                vect, distance = vector(pos, aim_pos)
                heappush(_vectors[vect], (distance, aim_pos))
            return _vectors

        best_pos, best_vectors = None, None
        for pos, c in np.ndenumerate(self.map):
            if c == '.':
                continue
            vectors = vectorize()
            if best_pos is None or len(best_vectors) < len(vectors):
                best_pos = pos
                best_vectors = vectors
        return best_pos, best_vectors

    @staticmethod
    def clockwise_angle(vector):
        ref_vec = [-1, 0]
        dot_prod = vector[0] * ref_vec[0] + vector[1] * ref_vec[1]  # x1*x2 + y1*y2
        diff_prod = ref_vec[1] * vector[0] - ref_vec[0] * vector[1]  # x1*y2 - y1*x2
        angle = math.atan2(diff_prod, dot_prod)
        if angle < 0:
            angle += 2 * math.pi
        return angle

    def part_a_b(self):
        station_pos, visible = self.find_monitoring_station()
        part_a = len(visible)

        it_ordered = it.cycle(sorted(visible.keys(), key=self.clockwise_angle))
        y, x = None, None
        for _ in range(200):
            while not visible.get((pos := next(it_ordered))):
                pass
            _, (y, x) = heappop(visible[pos])
        part_b = x * 100 + y

        return part_a, part_b


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day10)
