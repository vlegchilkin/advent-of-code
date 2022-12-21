from aoc import Input


class Solution:
    def __init__(self, inp: Input):
        input_lines = inp.get_lines()

        self.timeline = [1]
        for line in input_lines:
            self.timeline.append(self.timeline[-1])
            if line != "noop":
                self.timeline.append(self.timeline[-1] + (int(line.split(" ")[1])))

    def part_a(self):
        cycles = [20 + i * 40 for i in range(6)]
        part_a = sum([self.timeline[c - 1] * c for c in cycles])
        return part_a

    def part_b(self):
        crt = [[], [], [], [], [], []]
        for i in range(40 * 6):
            pixel = "#" if i % 40 in (self.timeline[i] - 1, self.timeline[i], self.timeline[i] + 1) else "."
            crt[i // 40].append(pixel)
        return "\n".join([" ".join(line) for line in crt]) + "\n"


def test_simple():
    solution = Solution(Input(1))
    assert solution.part_a() == 13140
    assert (
        solution.part_b()
        == """\
# # . . # # . . # # . . # # . . # # . . # # . . # # . . # # . . # # . . # # . .
# # # . . . # # # . . . # # # . . . # # # . . . # # # . . . # # # . . . # # # .
# # # # . . . . # # # # . . . . # # # # . . . . # # # # . . . . # # # # . . . .
# # # # # . . . . . # # # # # . . . . . # # # # # . . . . . # # # # # . . . . .
# # # # # # . . . . . . # # # # # # . . . . . . # # # # # # . . . . . . # # # #
# # # # # # # . . . . . . . # # # # # # # . . . . . . . # # # # # # # . . . . .
"""
    )


def test_puzzle():
    solution = Solution(Input())
    assert solution.part_a() == 13180
    assert (
        solution.part_b()
        == """\
# # # # . # # # # . # # # # . . # # . . # . . # . . . # # . . # # . . # # # . .
# . . . . . . . # . # . . . . # . . # . # . . # . . . . # . # . . # . # . . # .
# # # . . . . # . . # # # . . # . . . . # # # # . . . . # . # . . # . # # # . .
# . . . . . # . . . # . . . . # . . . . # . . # . . . . # . # # # # . # . . # .
# . . . . # . . . . # . . . . # . . # . # . . # . # . . # . # . . # . # . . # .
# # # # . # # # # . # . . . . . # # . . # . . # . . # # . . # . . # . # # # . .
"""
    )
