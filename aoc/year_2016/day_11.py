import collections
import copy
import itertools
import logging
import re

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2016Day11(Solution):
    """2016/11: Radioisotope Thermoelectric Generators"""

    def __init__(self, inp: Input):
        self.elements = dict()
        self.floors = []
        for line in inp.get_lines():
            s = line.split(" contains ")[1]
            items = re.findall(r"a (\w+)[- ](compatible microchip|generator)", s)
            floor = set()
            for item in items:
                s_id = self.elements.setdefault(item[0], len(self.elements) + 1)
                floor.add(s_id * (1 if item[1] == "generator" else -1))
            self.floors.append(floor)

    @staticmethod
    def find(elements, init_floors):
        def is_stable(p: set) -> bool:
            generators = {item for item in p if item > 0}
            for item in p:
                if item < 0 and -item not in generators and len(generators):
                    return False
            return True

        def _hash(grp: list[set], fl: int) -> int:
            """state of up to 7 elements and 4 floors might be packed into int64"""
            result = 1 << (14 * 4 + fl)
            for off, s in enumerate(grp):
                for i in s:
                    if i > 0:
                        result += 1 << (off * 14 + 7 + (i - 1))
                    else:
                        result += 1 << (off * 14 + (-i - 1))
            return result

        all_items = set(i * j for i in elements.values() for j in [-1, 1])
        final_hash = _hash([{}, {}, {}, all_items], len(init_floors) - 1)

        visited = {_hash(init_floors, 0)}
        q = collections.deque([(init_floors, 0, 0)])
        while q:
            floors, elevator, depth = q.popleft()

            # limiting the progress, remove to complete bfs without truncated paths
            if (d := depth // 5) >= 2 and len(floors[-1]) < d + 2:
                continue

            src_floor = floors[elevator]
            for direction in [-1, 1]:
                if not (0 <= (destination := elevator + direction) < len(floors)):
                    continue
                dst_floor = floors[destination]
                for count in [1, 2]:
                    if count > len(src_floor):
                        continue
                    for group in itertools.combinations(src_floor, count):
                        move_items = set(group)
                        if is_stable(_src := src_floor - move_items) and is_stable(_dst := dst_floor | move_items):
                            _floors = floors.copy()
                            _floors[elevator] = _src
                            _floors[destination] = _dst
                            if (r := _hash(_floors, destination)) not in visited:
                                if r == final_hash:
                                    logging.debug(f"Visited {len(visited)} states")
                                    return depth + 1
                                visited.add(r)
                                q.append((_floors, destination, depth + 1))

        return None

    def part_a(self):
        return self.find(self.elements, self.floors)

    def part_b(self):
        elements = copy.deepcopy(self.elements)
        elerium = elements["elerium"] = len(elements) + 1
        dilithium = elements["dilithium"] = len(elements) + 1
        floors = copy.deepcopy(self.floors)
        floors[0] |= {-elerium, elerium, -dilithium, dilithium}
        return self.find(elements, floors)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2016Day11)
