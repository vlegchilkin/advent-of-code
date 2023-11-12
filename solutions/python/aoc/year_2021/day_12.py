import collections
import pytest
from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2021Day12(Solution):
    def __init__(self, inp: Input):
        self.links = collections.defaultdict(lambda: [])
        for line in inp.get_lines(lambda x: x.split("-")):
            self.links[line[0]].append(line[1])
            self.links[line[1]].append(line[0])

    def paths(self, path, single_twice) -> int:
        if path[-1] == "end":
            return 1
        count = 0
        for node in self.links[path[-1]]:
            if node == "start":
                continue
            if node.isupper() or node not in path:
                count += self.paths(path + [node], single_twice)
            elif single_twice:
                count += self.paths(path + [node], False)
        return count

    def part_a(self):
        return self.paths(["start"], False)

    def part_b(self):
        return self.paths(["start"], True)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2021Day12)
