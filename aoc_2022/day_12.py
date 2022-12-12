from itertools import product
from collections import deque

import numpy as np

from aoc_2022 import Input, Spacer, D_BORDERS

if __name__ == "__main__":
    inp, (n, m) = Input().get_array()

    start = finish = None
    a = np.empty_like(inp, dtype=int)
    for x in product(range(n), range(m)):
        ch = inp[x]
        if ch == 'S':
            start = x
            ch = 'a'
        elif ch == 'E':
            finish = x
            ch = 'z'
        a[x] = ord(ch) - ord('a')

    v = np.full_like(a, fill_value=-1)
    v[finish] = 0

    spacer = Spacer(n, m, default_directions=D_BORDERS)
    q = deque([finish])
    while q:
        from_pos = q.popleft()
        for to_pos in spacer.get_links(*from_pos, test=lambda pos: v[pos] == -1):
            if a[from_pos] <= a[to_pos] + 1:
                v[to_pos] = v[from_pos] + 1
                q.append(to_pos)

    best = min([v[x] for x in product(range(n), range(m)) if v[x] >= 0 and a[x] == 0])
    print(f"part_a: {v[start]}")
    print(f"part_b: {best}")
