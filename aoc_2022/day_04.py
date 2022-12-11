import re

from aoc_2022 import Input

if __name__ == "__main__":
    part_a = part_b = 0
    r = re.compile(r'^(\d+)-(\d+),(\d+)-(\d+)$')
    for line in Input().get_lines():
        a0, a1, b0, b1 = list(map(int, r.match(line).groups()))
        if (a0 <= b0 <= a1) or (b0 <= a0 <= b1):
            part_b += 1
        if (a0 <= b0 and b1 <= a1) or (b0 <= a0 and a1 <= b1):
            part_a += 1
    print(part_a)
    print(part_b)
