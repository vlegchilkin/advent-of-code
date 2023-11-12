import copy
import re
from collections import Counter
from enum import StrEnum

import pytest
import dataclasses as dc

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Side(StrEnum):
    IMMUNE_SYSTEM = "Immune System"
    INFECTION = "Infection"


@dc.dataclass
class Group:
    id: tuple[Side, int]
    units: int
    hp: int
    immune: list[str]
    weak: list[str]
    attack_type: str
    damage: int
    initiative: int

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return (self.effective_power(), self.initiative) > (other.effective_power(), other.initiative)

    def effective_power(self):
        return self.units * self.damage


class Year2018Day24(Solution):
    """2018/24: Immune System Simulator 20XX"""

    def __init__(self, inp: Input):
        armies = inp.get_blocks()
        r = re.compile(
            r"^(\d+) units each with (\d+) hit points "
            r"(\((.*)\) )?"
            r"with an attack that does (\d+) (\w+) damage at initiative (\d+)$"
        )

        def parse_group(id, line):
            g = r.match(line).groups()
            immo_weak = {k: v.split(", ") for k, _, v in map(lambda s: s.partition(" to "), (g[-4] or "").split("; "))}
            return Group(
                id=id,
                units=int(g[0]),
                hp=int(g[1]),
                immune=immo_weak.get("immune") or [],
                weak=immo_weak.get("weak") or [],
                attack_type=g[-2],
                damage=int(g[-3]),
                initiative=int(g[-1]),
            )

        self.warriors = []
        for title, *definition in armies:
            for index, group in enumerate(definition):
                self.warriors.append(parse_group((Side(title[:-1]), index + 1), group))

    @staticmethod
    def simulate(warriors):
        def damage(attacker: Group, defender: Group):
            result = attacker.effective_power()
            if attacker.attack_type in defender.immune:
                result *= 0
            elif attacker.attack_type in defender.weak:
                result *= 2
            return result

        def most_damaged_defender(attacker: Group, occupied):
            best = (0, None)
            for defender in warriors:
                if defender.id[0] == attacker.id[0] or defender in occupied:
                    continue
                if (dmg := damage(attacker, defender)) > best[0]:
                    best = dmg, defender
            return best[1]

        def fight():
            targets = {}
            for attacker in warriors:
                defender = most_damaged_defender(attacker, targets.values())
                if defender:
                    targets[attacker] = defender

            if not targets:
                return False

            for attacker, defender in sorted(targets.items(), key=lambda a: a[0].initiative, reverse=True):
                if attacker.units <= 0:
                    continue
                defender.units -= damage(attacker, defender) // defender.hp
                if defender.units <= 0:
                    warriors.remove(defender)
            return True

        while len(Counter(w.id[0] for w in warriors)) == 2:
            warriors = sorted(warriors)
            if not fight():
                break
        return warriors

    def part_a(self):
        warriors = self.simulate(copy.deepcopy(self.warriors))
        return sum(w.units for w in warriors)

    def part_b(self):
        def try_boosted(boost):
            warriors = copy.deepcopy(self.warriors)
            for warrior in warriors:
                if warrior.id[0] == Side.IMMUNE_SYSTEM:
                    warrior.damage += boost
            return self.simulate(warriors)

        low, high = 0, 100_000
        while low < high:
            mid = (low + high) // 2
            if all(warrior.id[0] == Side.IMMUNE_SYSTEM for warrior in try_boosted(mid)):
                high = mid
            else:
                low = mid + 1
        return sum(w.units for w in try_boosted(high))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day24)
