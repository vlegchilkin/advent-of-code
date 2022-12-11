import copy
import re
import string

from aoc_2022 import Input

r = re.compile(r'^move (\d+) from (\d+) to (\d+)$')

if __name__ == "__main__":
    stacks = None
    input_iter = Input().get_iter()
    while (line := next(input_iter, None)) and (line[1] != "1"):
        if not stacks:
            stacks = [[] for _ in range((len(line) + 1) // 4)]
        for i in range(0, len(stacks)):
            if (e := line[i * 4 + 1]) in string.ascii_uppercase:
                stacks[i].insert(0, e)

    next(input_iter)

    part_a, part_b = stacks, copy.deepcopy(stacks)
    for line in input_iter:
        count, f, t = list(map(int, r.match(line).groups()))

        part_b[t - 1].extend(part_b[f - 1][-count:])
        del part_b[f - 1][-count:]

        part_a[t - 1].extend(reversed(part_a[f - 1][-count:]))
        del part_a[f - 1][-count:]

    print("".join([stack[-1] for stack in part_a if stack]))
    print("".join([stack[-1] for stack in part_b if stack]))
