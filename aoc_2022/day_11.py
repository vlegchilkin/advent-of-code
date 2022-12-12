import copy
import math

from aoc_2022 import Input


def test(monkey, value, reduce_factor) -> (int, int):
    op_value = monkey.op_right if monkey.op_right else value
    if monkey.op_sign == '+':
        new_value = value + op_value
    else:
        new_value = value * op_value

    if reduce_factor:
        new_value = new_value // reduce_factor

    return (
        new_value % lcm,
        monkey.if_true if new_value % monkey.test == 0 else monkey.if_false
    )


def turn(monkeys, reduce_factor):
    for monkey in monkeys:
        for value in monkey.worries:
            new_value, direction = test(monkey, value, reduce_factor)
            monkeys[direction].worries.append(new_value)
        monkey.turns += len(monkey.worries)
        monkey.worries = []


def simulate(monkeys, iterations, reduce_factor: int = None):
    for i in range(iterations):
        turn(monkeys, reduce_factor)
        if i == 19 or (i + 1) % 1000 == 0:
            turns = [m.turns for m in monkeys]
            print(f"{i + 1}: {turns}")

    turns = sorted([m.turns for m in monkeys], reverse=True)
    print(f"-> {turns[0] * turns[1]}")


ttp_template = """\
Monkey {{ id | to_int | let(turns, 0) }}: 
  Starting items: {{ worries | ORPHRASE | to_int_list }} 
  Operation: new = old {{ op_sign }} {{ op_right | to_optional_int("old") }}
  Test: divisible by {{ test | to_int }}
    If true: throw to monkey {{ if_true | to_int }} 
    If false: throw to monkey {{ if_false | to_int }}
"""

if __name__ == "__main__":
    input_monkeys = Input().get_objects(ttp_template)
    input_monkeys.sort(key=lambda m: m.id)
    lcm = math.lcm(*[m.test for m in input_monkeys])
    print("part_a:")
    simulate(copy.deepcopy(input_monkeys), 20, 3)

    print("part_b:")
    simulate(copy.deepcopy(input_monkeys), 10000)
