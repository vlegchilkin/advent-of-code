from collections import deque

from aoc_2022 import Input, Spacer, D_BORDERS

if __name__ == "__main__":
    inp, (n, m) = Input().get_array()
    spacer = Spacer(n, m, default_directions=D_BORDERS)

    start = finish = None
    a = spacer.new_array(0)
    for x in spacer.iter():
        ch = inp[x]
        if ch == "S":
            start = x
            ch = "a"
        elif ch == "E":
            finish = x
            ch = "z"
        a[x] = ord(ch) - ord("a")

    visited = spacer.new_array(-1)
    visited[finish] = 0

    queue = deque([finish])
    while queue:
        from_pos = queue.popleft()
        for to_pos in spacer.get_links(from_pos):
            if visited[to_pos] == -1 and a[from_pos] <= a[to_pos] + 1:
                visited[to_pos] = visited[from_pos] + 1
                queue.append(to_pos)

    best = min([visited[x] for x in spacer.iter(lambda pos: visited[pos] != -1 and a[pos] == 0)])
    print(f"part_a: {visited[start]}")
    print(f"part_b: {best}")
