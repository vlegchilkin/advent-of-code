import dataclasses
from dataclasses import dataclass
from typing import Optional, Tuple

import pytest
from numpy import PINF

from aoc import Input, get_puzzles, PuzzleData


@dataclass(frozen=True)
class Spell:
    name: str
    mana: int
    damage: int = 0
    active_turns: int = None
    armor: int = 0
    hp_restore: int = 0
    mana_restore: int = 0


SPELLS = [
    Spell("Poison", 173, damage=3, active_turns=6),
    Spell("Recharge", 229, mana_restore=101, active_turns=5),
    Spell("Shield", 113, armor=7, active_turns=6),
    Spell("Magic Missile", 53, damage=4),
    Spell("Drain", 73, damage=2, hp_restore=2),
]


@dataclass(frozen=True)
class Fighter:
    hp: int
    mana: int = 0
    physical_damage: int = 0
    bleeding: bool = False
    effects: dict[Spell, int] = dataclasses.field(default_factory=lambda: dict())

    def armor(self) -> int:
        return sum(map(lambda s: s.armor, self.effects))

    def damage(self) -> int:
        return self.physical_damage + sum(map(lambda s: s.damage, self.effects))

    def cast(self, rival: "Fighter", spell: Spell) -> Optional[Tuple["Fighter", "Fighter"]]:
        if spell.active_turns:
            if spell in self.effects:
                return None
            side_effects = {spell: spell.active_turns}
        else:
            side_effects = {}

        insta_damage = spell.damage if not spell.active_turns else 0
        return (
            Fighter(
                hp=self.hp + (spell.hp_restore if not spell.active_turns else 0),
                physical_damage=self.physical_damage,
                mana=self.mana - spell.mana + (spell.mana_restore if not spell.active_turns else 0),
                effects=self.effects | side_effects,
                bleeding=self.bleeding,
            ),
            rival.bleed(insta_damage) if insta_damage else rival,
        )

    def defend(self, rival: "Fighter") -> "Fighter":
        return Fighter(
            hp=self.hp - max(1 if rival.physical_damage else 0, rival.damage() - self.armor()),
            physical_damage=self.physical_damage,
            mana=self.mana,
            effects=self.effects,
            bleeding=self.bleeding,
        )

    def bleed(self, hp=1) -> "Fighter":
        return Fighter(
            hp=self.hp - hp,
            physical_damage=self.physical_damage,
            mana=self.mana,
            effects=self.effects,
            bleeding=self.bleeding,
        )

    def process_effects(self) -> "Fighter":
        return Fighter(
            hp=self.hp + sum(map(lambda s: s.hp_restore, self.effects)),
            mana=self.mana + sum(map(lambda s: s.mana_restore, self.effects)),
            physical_damage=self.physical_damage,
            effects={spell: turns - 1 for spell, turns in self.effects.items() if turns > 1},
            bleeding=self.bleeding,
        )


class Solution:
    def __init__(self, inp: Input):
        boss_lines = inp.get_objects("{{property|ORPHRASE}}: {{value|to_int}}")
        boss_stats = {line.property: line.value for line in boss_lines}
        self.boss = Fighter(hp=boss_stats["Hit Points"], physical_damage=boss_stats["Damage"])

    def recu(self, player: Fighter, boss: Fighter, player_turn: bool, mana_cost: int, best) -> Optional[int]:
        if player.bleeding and player_turn:
            if (player := player.bleed()).hp <= 0:
                return None

        boss = boss.defend(player)  # effects damage
        if boss.hp <= 0:
            return mana_cost

        if not player_turn:
            player = player.defend(boss)

        if (player := player.process_effects()).hp <= 0:
            return None

        if not player_turn:
            return self.recu(player, boss, True, mana_cost, best)

        for spell in SPELLS:
            if spell.mana > player.mana or (cost := mana_cost + spell.mana) >= best:
                continue
            if not (cast_result := player.cast(boss, spell)):
                continue

            if cast_result[1].hp > 0:
                current_costs = self.recu(*cast_result, player_turn=False, mana_cost=cost, best=best)
            else:
                current_costs = cost

            if current_costs is not None and best > current_costs:
                best = current_costs

        return best

    def part_a(self):
        return self.recu(Fighter(50, mana=500), self.boss, True, 0, PINF)

    def part_b(self):
        return self.recu(Fighter(50, mana=500, bleeding=True), self.boss, True, 0, PINF)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
