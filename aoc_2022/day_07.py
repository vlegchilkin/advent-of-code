from aoc_2022 import Input


def part_a_sol(node) -> int:
    result = t if (t := node["total"]) < 100000 else 0

    for v in node["children"].values():
        result += part_a_sol(v)

    return result


def part_b_sol(node, goal) -> int:
    best = t if (t := node["total"]) >= goal else None

    for v in node["children"].values():
        if (_best := part_b_sol(v, goal)) and (not best or _best < best):
            best = _best

    return best


def count_total(node) -> int:
    result = node["files_size"] if "files_size" in node else 0

    for v in node["children"].values():
        result += count_total(v)

    node["total"] = result
    return result


if __name__ == "__main__":
    input_iter = Input().get_iter()

    root = node = {"children": {}}
    line = next(input_iter)
    while line:
        if line.startswith("$ cd"):
            if (name := line[5:]) == "..":
                node = node["parent"]
            else:
                if name not in node["children"]:
                    child = {"parent": node, "children": {}}
                    node["children"][name] = child
                    node = child
                else:
                    node = node["children"][name]
            line = next(input_iter, None)
        elif line.startswith("$ ls"):
            total = 0
            while (line := next(input_iter, None)) and not line.startswith("$"):
                if not line.startswith("dir "):
                    size, _ = line.split(" ")
                    total += int(size)
            node["files_size"] = total

    count_total(root)

    part_a = part_a_sol(root)
    print(f"part a: {part_a}")
    need = 30000000 - (70000000 - root["total"])
    print(f"need space: {need}")
    print(f"part b: {part_b_sol(root, need)}")
