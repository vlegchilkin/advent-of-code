import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        data = inp.get_lists("Sue {{id | to_int}}: {{ values | ORPHRASE | split(', ')}}")

        def parse(groups):
            return {g[0]: int(g[1]) for g in [group.split(": ") for group in groups]}

        self.aunts = {name: parse(groups) for name, groups in data}
        self.state = {o.name: o.value for o in Input(0).get_objects("{{name}}: {{value | to_int}}")}

    def part_a(self):
        for aunt_id, aunt_items in self.aunts.items():
            for item, value in aunt_items.items():
                if self.state.get(item) != value:
                    break
            else:
                return aunt_id

    def part_b(self):
        for aunt_id, aunt_items in self.aunts.items():
            for item, value in aunt_items.items():
                if item in ["cats", "trees"]:
                    if self.state.get(item) >= value:
                        break
                elif item in ["pomeranians", "goldfish"]:
                    if self.state.get(item) <= value:
                        break
                else:
                    if self.state.get(item) != value:
                        break
            else:
                return aunt_id


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
