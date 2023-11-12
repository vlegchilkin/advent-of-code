import dataclasses
from dataclasses import dataclass
from itertools import combinations
from typing import Optional

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, dataclass_by_template, Solution


@dataclass
class Item:
    name: str
    cost: int
    damage: int
    armor: int


@dataclass
class Stats:
    hp: int
    damage: int = 0
    armor: int = 0
    costs: int = 0

    def with_item(self, item: Item):
        return dataclasses.replace(
            self, damage=self.damage + item.damage, armor=self.armor + item.armor, costs=self.costs + item.cost
        )


class Year2015Day21(Solution):
    def __init__(self, inp: Input):
        def parse(itm: str) -> Item:
            ttp_template = "{{name|ORPHRASE}} {{cost|to_int}} {{damage|to_int}} {{armor|to_int}}"
            return dataclass_by_template(Item, itm, ttp_template)

        weapons, armors, rings = Input(0).get_blocks()
        self.weapons = [parse(item) for item in weapons[1:]]
        self.armors = [parse(item) for item in armors[1:]]
        self.rings = [parse(item) for item in rings[1:]]

        boss_lines = inp.get_objects("{{property|ORPHRASE}}: {{value|to_int}}")
        boss_stats = {line.property: line.value for line in boss_lines}
        self.boss = Stats(boss_stats["Hit Points"], boss_stats["Damage"], boss_stats["Armor"])

    @staticmethod
    def simulate(player: Stats, boss: Stats) -> bool:
        players = [dataclasses.replace(player), dataclasses.replace(boss)]
        active = 0
        while players[0].hp * players[1].hp > 0:
            players[1 - active].hp -= max(1, players[active].damage - players[1 - active].armor)
            active = 1 - active
        return players[0].hp > players[1].hp

    def recu(self, stage, stats: Stats, expected_win: bool) -> Optional[int]:
        best = None

        def try_items(items, min_count, max_count):
            nonlocal best
            for count in range(min_count, max_count + 1):
                for it in combinations(items, count):
                    st = stats
                    for c in range(count):
                        st = st.with_item(it[c])
                    current = self.recu(stage + 1, st, expected_win)
                    if best is None:
                        best = current
                    elif current is not None:
                        best = min(best, current) if expected_win else max(best, current)

        match stage:
            case 0:
                try_items(self.weapons, 1, 1)
            case 1:
                try_items(self.armors, 0, 1)
            case 2:
                try_items(self.rings, 0, 2)
            case 3:
                player_win = self.simulate(stats, self.boss)
                if player_win == expected_win:
                    best = stats.costs
        return best

    def part_a(self):
        return self.recu(0, Stats(hp=100), True)

    def part_b(self):
        return self.recu(0, Stats(hp=100), False)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2015Day21)
