import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2015Day14(Solution):
    def __init__(self, inp: Input):
        self.players = inp.get_objects(
            "{{ name }} can fly {{ speed | to_int}} km/s for {{ active_time | to_int }} seconds, "
            "but then must rest for {{ rest_time | to_int}} seconds."
        )

    @staticmethod
    def _distance(player, time_limit):
        cycle_len = player.active_time + player.rest_time
        fly_time = (time_limit // cycle_len) * player.active_time + min(time_limit % cycle_len, player.active_time)
        return fly_time * player.speed

    def part_a(self):
        return max([self._distance(p, 2503) for p in self.players])

    def part_b(self):
        points = {player.name: 0 for player in self.players}
        for time in range(1, 2504):
            best_names, best_distance = {}, None
            for player in self.players:
                distance = self._distance(player, time)
                if best_distance is None or best_distance < distance:
                    best_names = {player.name}
                    best_distance = distance
                elif best_distance == distance:
                    best_names.add(player.name)
            for name in best_names:
                points[name] += 1
        return max(points.values())


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2015Day14)
