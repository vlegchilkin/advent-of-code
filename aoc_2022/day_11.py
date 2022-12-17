import copy
import math

from aoc_2022 import Input

TTP_TEMPLATE = """\
Monkey {{ id | to_int | let(turns, 0) }}: 
  Starting items: {{ worries | ORPHRASE | to_int_list }} 
  Operation: new = old {{ op_sign }} {{ op_right | to_optional_int("old") }}
  Test: divisible by {{ test | to_int }}
    If true: throw to monkey {{ if_true | to_int }} 
    If false: throw to monkey {{ if_false | to_int }}
"""


class Solution:
    def __init__(self, inp: Input):
        self.input_monkeys = inp.get_objects(TTP_TEMPLATE)
        self.input_monkeys.sort(key=lambda m: m.id)
        self.lcm = math.lcm(*[m.test for m in self.input_monkeys])

    def test(self, monkey, value, reduce_factor) -> (int, int):
        op_value = monkey.op_right if monkey.op_right else value
        if monkey.op_sign == "+":
            new_value = value + op_value
        else:
            new_value = value * op_value

        if reduce_factor:
            new_value = new_value // reduce_factor

        return new_value % self.lcm, monkey.if_true if new_value % monkey.test == 0 else monkey.if_false

    def turn(self, monkeys, reduce_factor):
        for monkey in monkeys:
            for value in monkey.worries:
                new_value, direction = self.test(monkey, value, reduce_factor)
                monkeys[direction].worries.append(new_value)
            monkey.turns += len(monkey.worries)
            monkey.worries = []

    def simulate(self, monkeys, iterations, reduce_factor: int = None):
        for i in range(iterations):
            self.turn(monkeys, reduce_factor)
            if i == 19 or (i + 1) % 1000 == 0:
                turns = [m.turns for m in monkeys]
                print(f"{i + 1}: {turns}")

        turns = sorted([m.turns for m in monkeys], reverse=True)
        return turns[0] * turns[1]

    def part_a(self):
        return self.simulate(copy.deepcopy(self.input_monkeys), 20, 3)

    def part_b(self):
        return self.simulate(copy.deepcopy(self.input_monkeys), 10000)


def test_simple():
    solution = Solution(Input(0))
    assert solution.part_a() == 10605
    assert solution.part_b() == 2713310158


def test_challenge():
    solution = Solution(Input())
    assert solution.part_a() == 119715
    assert solution.part_b() == 18085004878
