import copy

from aoc_2022 import Input

TTP_TEMPLATE = """{{ monkey }}: {{ operation | ORPHRASE  | split(" ")}}"""


class Solution:
    def __init__(self, inp: Input):
        self.inputs = {
            obj.monkey: tuple(obj.operation) if len(obj.operation) > 1 else int(obj.operation[0])
            for obj in inp.get_objects(TTP_TEMPLATE)
        }

    def pre_solve(self, monkeys, monkey):
        value = monkeys[monkey]
        if type(value) != tuple:
            return value

        left = self.pre_solve(monkeys, value[0]) if type(value[0]) == str else value[0]
        right = self.pre_solve(monkeys, value[2]) if type(value[2]) == str else value[2]

        if type(left) == type(right) == int:
            match value[1]:
                case "+":
                    total = left + right
                case "-":
                    total = left - right
                case "*":
                    total = left * right
                case "/":
                    total = left // right
                case _:
                    raise ValueError(f"Non-supported operation: {value[1]}")
        else:
            total = [value[1], left, right]

        monkeys[monkey] = total
        return total

    def part_a(self):
        return self.pre_solve(copy.deepcopy(self.inputs), "root")

    def solve(self, eq, match=None):
        if eq == "X":
            return match
        first_known = type(eq[1]) == int
        next_eq = eq[2] if first_known else eq[1]
        match eq[0]:
            case "=":
                next_match = eq[1] if first_known else eq[2]
            case "+":
                next_match = match - eq[1] if first_known else match - eq[2]
            case "-":
                next_match = eq[1] - match if first_known else match + eq[2]
            case "*":
                next_match = match // eq[1] if first_known else match // eq[2]
            case "/":
                next_match = eq[1] // match if first_known else match * eq[2]
            case _:
                raise ValueError(f"Non-supported operation {eq[0]}")

        return self.solve(next_eq, next_match)

    def part_b(self):
        monkeys = copy.deepcopy(self.inputs)
        monkeys["humn"] = "X"
        monkeys["root"] = (monkeys["root"][0], "=", monkeys["root"][2])
        equation = self.pre_solve(monkeys, "root")
        return self.solve(equation)


def test_simple():
    solution = Solution(Input(0))
    assert solution.part_a() == 152
    assert solution.part_b() == 301


def test_challenge():
    solution = Solution(Input())
    assert solution.part_a() == 70674280581468
    assert solution.part_b() == 3243420789721
