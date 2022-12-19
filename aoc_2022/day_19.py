import time

import math

from aoc_2022 import Input, t_sum, t_koef

TTP_TEMPLATE = """\
Blueprint {{ id | to_int}}: \
Each ore robot costs {{ ore_ore | to_int }} ore. \
Each clay robot costs {{ clay_ore | to_int }} ore. \
Each obsidian robot costs {{ obs_ore | to_int }} ore and {{ obs_clay | to_int }} clay. \
Each geode robot costs {{ geode_ore | to_int }} ore and {{ geode_obs | to_int }} obsidian.
"""


class Solution:
    def __init__(self, inp: Input):
        self.blueprints = inp.get_objects(TTP_TEMPLATE)

    def _workdays(self, need_a, robot_a, need_b=None, robot_b=None):
        if need_a > 0:
            return 1 + max(math.ceil(need_a / robot_a), math.ceil(need_b / robot_b) if need_b and need_b > 0 else 0)
        elif need_b > 0:
            return 1 + math.ceil(need_b / robot_b)
        else:
            return 1

    def f(self, bp, robots, resources, days, warmup, robo_limit) -> int:
        best = resources[3] + (days * robots[3])

        if robo_limit[1]:
            if (workdays := self._workdays(bp.clay_ore - resources[0], robots[0], 0, 0)) <= days:
                new_resources = t_sum(resources, t_koef(workdays, robots))
                new_resources = t_sum(new_resources, (-bp.clay_ore, 0, 0, 0))
                best = max(best, self.f(bp, t_sum(robots, (0, 1, 0, 0)), new_resources, days - workdays, warmup-1, t_sum(robo_limit, (0, -1, 0, 0))))

        if robo_limit[0]:
            if (workdays := self._workdays(bp.ore_ore - resources[0], robots[0], 0, 0)) <= days:
                new_resources = t_sum(resources, t_koef(workdays, robots))
                new_resources = t_sum(new_resources, (-bp.ore_ore, 0, 0, 0))
                best = max(best, self.f(bp, t_sum(robots, (1, 0, 0, 0)), new_resources, days - workdays, warmup-1, t_sum(robo_limit, (-1, 0, 0, 0))))

        if warmup > 0:
            return best

        if robo_limit[3] and robots[2]:
            workdays = self._workdays(
                bp.geode_obs - resources[2], robots[2], bp.geode_ore - resources[0], robots[0]
            )
            if workdays <= days:
                new_resources = t_sum(resources, t_koef(workdays, robots))
                new_resources = t_sum(new_resources, (-bp.geode_ore, 0, -bp.geode_obs, 0))
                best = max(
                    best, self.f(bp, t_sum(robots, (0, 0, 0, 1)), new_resources, days - workdays, warmup-1,  t_sum(robo_limit, (0, 0, 0, -1)))
                )

        if robo_limit[2] and robots[1]:
            workdays = self._workdays(bp.obs_clay - resources[1], robots[1], bp.obs_ore - resources[0], robots[0])
            if workdays <= days:
                new_resources = t_sum(resources, t_koef(workdays, robots))
                new_resources = t_sum(new_resources, (-bp.obs_ore, -bp.obs_clay, 0, 0))
                best = max(
                    best, self.f(bp, t_sum(robots, (0, 0, 1, 0)), new_resources, days - workdays, warmup-1, t_sum(robo_limit, (0, 0, -1, 0)))
                )

        return best

    def part_a(self) -> tuple[int, list[int]]:
        print('Part A:')
        values = []
        result = 0
        for i, blueprint in enumerate(self.blueprints):
            warmup = math.ceil((blueprint.geode_obs + blueprint.obs_clay) // 8)
            robot_limits = (3, 9 if blueprint.clay_ore < 3 else 8, 6, 6)
            value = self.check_conditions(blueprint, robot_limits, warmup=warmup, length=24)
            values.append(value)
            result += value * blueprint.id
        return result, values

    def part_b(self) -> tuple[int, list[int]]:
        print('Part B:')
        result = 1
        values = []
        for blueprint in self.blueprints:
            if blueprint.id > 3:
                break
            value = self.check_conditions(blueprint, robo_limit=(3, 11, 10, 10), warmup=9, length=32)
            result *= value
            values.append(value)
        return result, values

    def check_conditions(self, blueprint, robo_limit, warmup, length):
        start_time = time.time()
        value = self.f(blueprint, (1, 0, 0, 0), (0, 0, 0, 0), length, warmup, robo_limit)
        print(f"{blueprint.id}: {value} at {time.time() - start_time}")
        return value


def test_simple():
    """
        Blueprint_2: 12 [ 'Day: 3, ore', 'Day: 5, ore', 'Day: 6, clay', 'Day: 7, clay', 'Day: 8, clay', 'Day: 9, clay',
        'Day: 10, clay', 'Day: 11, obs', 'Day: 13, obs', 'Day: 14, obs', 'Day: 16, obs', 'Day: 17, obs',
        'Day: 18, geode', 'Day: 19, obs', 'Day: 20, geode', 'Day: 22, geode']
    :return:
    """
    solution = Solution(Input(0))
    assert solution.part_a() == (33, [9, 12])
    assert solution.part_b() == (3472, [56, 62])


def test_challenge():
    solution = Solution(Input())
    assert solution.part_a() == (
        1418,
        [0, 1, 0, 0, 1, 2, 2, 11, 0, 12, 0, 0, 0, 0, 0, 3, 0, 2, 3, 5, 2, 2, 4, 1, 9, 12, 3, 0, 4, 0],
    )
    assert solution.part_b() == (4114, [11, 22, 17])
