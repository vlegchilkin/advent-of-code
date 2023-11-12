import dataclasses
from dataclasses import dataclass
from typing import Optional, Tuple

import pytest
from numpy import PINF

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


@dataclass(frozen=True)
class Spell:
    name: str
    mana: int
    damage: int = 0
    effect_turns: Optional[int] = None
    armor: int = 0
    hp_restore: int = 0
    mana_restore: int = 0


SPELLS = [
    Spell("Poison", 173, damage=3, effect_turns=6),
    Spell("Recharge", 229, mana_restore=101, effect_turns=5),
    Spell("Shield", 113, armor=7, effect_turns=6),
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
        if spell.mana > self.mana:
            return
        if spell.effect_turns:
            if spell in self.effects:
                return  # rule: don't apply already applied effects
            effects = self.effects | {spell: spell.effect_turns}
        else:
            effects = self.effects

        insta_damage = spell.damage if not spell.effect_turns else 0
        return (
            dataclasses.replace(
                self,
                hp=self.hp + (spell.hp_restore if not spell.effect_turns else 0),
                mana=self.mana - spell.mana + (spell.mana_restore if not spell.effect_turns else 0),
                effects=effects,
            ),
            rival.bleed(insta_damage) if insta_damage else rival,
        )

    def defend(self, rival: "Fighter") -> "Fighter":
        lost_hp = max(1 if rival.physical_damage else 0, rival.damage() - self.armor())
        return self.bleed(lost_hp)

    def bleed(self, hp_loss=1) -> "Fighter":
        return dataclasses.replace(self, hp=self.hp - hp_loss) if hp_loss > 0 else self

    def process_effects(self) -> "Fighter":
        return dataclasses.replace(
            self,
            hp=self.hp + sum(map(lambda s: s.hp_restore, self.effects)),
            mana=self.mana + sum(map(lambda s: s.mana_restore, self.effects)),
            effects={spell: turns - 1 for spell, turns in self.effects.items() if turns > 1},
        )


class Year2015Day22(Solution):
    def __init__(self, inp: Input):
        boss_lines = inp.get_objects("{{property|ORPHRASE}}: {{value|to_int}}")
        boss_stats = {line.property: line.value for line in boss_lines}
        self.boss = Fighter(hp=boss_stats["Hit Points"], physical_damage=boss_stats["Damage"])

    def recu(self, player: Fighter, boss: Fighter, player_turn: bool, mana_cost: int, best) -> Optional[int]:
        n_player = player
        if player.bleeding and player_turn:
            if (n_player := n_player.bleed()).hp <= 0:
                return best

        n_boss = boss.defend(n_player)  # effects damage
        if n_boss.hp <= 0:
            return mana_cost

        if not player_turn:
            n_player = n_player.defend(n_boss)

        if (n_player := n_player.process_effects()).hp <= 0:
            return best

        if not player_turn:
            return self.recu(n_player, n_boss, True, mana_cost, best)

        good_spells = ((spell, cost) for spell in SPELLS if (cost := mana_cost + spell.mana) < best)
        for spell, cost in good_spells:
            if not (cr := n_player.cast(n_boss, spell)):
                continue
            if cr[1].hp > 0:
                best = min(best, self.recu(*cr, player_turn=False, mana_cost=cost, best=best))
            else:
                best = min(best, cost)

        return best

    def part_a(self):
        return self.recu(Fighter(50, mana=500), self.boss, True, 0, PINF)

    def part_b(self):
        return self.recu(Fighter(50, mana=500, bleeding=True), self.boss, True, 0, PINF)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2015Day22)
