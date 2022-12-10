import math
import string
from functools import reduce

from aoc_2022 import get_input_lines


def sol(items) -> int:
    def f(s) -> int:
        return reduce(lambda x, y: x | y, [1 << string.ascii_letters.index(c) for c in s])

    return int(math.log(reduce(lambda x, y: x & y, [f(item) for item in items]), 2)) + 1


if __name__ == "__main__":
    lines = get_input_lines()

    total_a = sum([sol([line[:len(line) // 2], line[len(line) // 2:]]) for line in lines])
    total_b = sum([sol(lines[i:i + 3]) for i in range(0, len(lines), 3)])

    print(f"part_a: {total_a}")
    print(f"part_b: {total_b}")
