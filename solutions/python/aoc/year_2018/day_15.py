import dataclasses as dc
from enum import StrEnum
from typing import Optional, Callable

import pytest
from numpy import Inf

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import Spacer, C, to_t


class Race(StrEnum):
    ELF = "E"
    GOBLIN = "G"


@dc.dataclass
class Creature:
    id: int = dc.field(hash=True, compare=True)
    race: Race
    hp: int


class Year2018Day15(Solution):
    """2018/15: Beverage Bandits"""

    def __init__(self, inp: Input):
        self.data = inp.get_array(lambda d: d if d != "." else None)
        self.base_health = 200

    def combat(self, race_attack: dict[Race, int], elf_first_blood_mode=False):
        maze = Spacer.build(self.data, directions=[C.NORTH, C.WEST, C.EAST, C.SOUTH])
        creatures = {}
        for cord, v in list(maze):
            if v in iter(Race):
                del maze[cord]
                creatures[cord] = Creature(len(creatures) + 1, Race(v), self.base_health)

        def is_enemy_checker(creature: Creature) -> Callable[[complex], bool]:
            return lambda p: (a := creatures.get(p)) and a.race != creature.race

        def enemy_nearby(pos, creature: Creature):
            enemy_pos, enemy = None, None
            for link in maze.links(pos, has_path=is_enemy_checker(creature)):
                e = creatures[link]
                if enemy is None or enemy.hp > e.hp:
                    enemy_pos, enemy = link, e
            if enemy:
                return enemy_pos, enemy

        def find_move(pos, creature) -> Optional[complex]:
            d, _ = maze.bfs(pos, has_path=lambda p: p not in maze and p not in creatures)
            closest_spot = (Inf, None)
            for enemy_pos in [_pos for _pos, c in creatures.items() if c.race != creature.race]:
                for link in maze.links(enemy_pos, has_path=lambda p: p in d):
                    if (spot := (d[link][0], to_t(link))) < closest_spot:
                        closest_spot = spot

            if closest_spot[1] is None:
                return

            aim = complex(*closest_spot[1])
            while (backtrack := d[aim][1]) != pos:
                aim = backtrack

            return aim

        def single_round():
            for pos, creature in sorted(creatures.items(), key=lambda c: (c[0].real, c[0].imag)):
                if creature.hp <= 0:
                    continue
                if not any(c for c in creatures.values() if c.race != creature.race):
                    return creature.race

                if (enemy := enemy_nearby(pos, creature)) is None:
                    if _pos := find_move(pos, creature):
                        del creatures[pos]
                        creatures[_pos] = creature
                        pos = _pos
                    else:
                        continue

                if enemy or (enemy := enemy_nearby(pos, creature)):
                    enemy[1].hp -= race_attack[creature.race]
                    if enemy[1].hp <= 0:
                        del creatures[enemy[0]]
                        if enemy[1].race == Race.ELF and elf_first_blood_mode:
                            return Race.GOBLIN

        for t in range(0, 1_000):  # infinite loop brake
            if win := single_round():
                return win, t * sum(c.hp for c in creatures.values())

    def part_a(self):
        _, score = self.combat({Race.GOBLIN: 3, Race.ELF: 3})
        return score

    def part_b(self):
        for elf_attack in range(4, self.base_health + 1):
            win, score = self.combat({Race.GOBLIN: 3, Race.ELF: elf_attack}, elf_first_blood_mode=True)
            if win == Race.ELF:
                return score


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day15)
