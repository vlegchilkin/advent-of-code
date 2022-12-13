import json
from functools import cmp_to_key

import math

from aoc_2022 import Input


def cmp(left, right) -> int:
    l_int, r_int = isinstance(left, int), isinstance(right, int)
    if l_int and r_int:
        return left - right

    left = [left] if l_int else left
    right = [right] if r_int else right

    for left_v, right_v in zip(left, right):
        if c := cmp(left_v, right_v):
            return c

    return len(left) - len(right)


if __name__ == "__main__":
    lists = [json.loads(line) for line in Input().get_iter() if line]
    part_a = 0
    for i in range(0, len(lists), 2):
        if cmp(lists[i], lists[i + 1]) < 0:
            part_a += (i // 2 + 1)
    print(f"part_a: {part_a}")

    markers = [[[2]], [[6]]]
    lists.extend(markers)
    lists = sorted(lists, key=cmp_to_key(cmp))
    part_b = math.prod([(i + 1) for i, v in enumerate(lists) if v in markers])
    print(f"part_b: {part_b}")
