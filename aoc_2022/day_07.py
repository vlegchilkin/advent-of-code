from aoc_2022 import Input


class Solution:
    def __init__(self, inp: Input):
        input_iter = inp.get_iter()

        self.root = node = {"children": {}}
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
            else:
                raise ValueError(f"Wrong Input: {line}")

        self._count_total(self.root)

    def _count_total(self, node) -> int:
        result = node["files_size"] if "files_size" in node else 0

        for v in node["children"].values():
            result += self._count_total(v)

        node["total"] = result
        return result

    def part_a(self):
        return self._part_a_sol(self.root)

    def _part_a_sol(self, node) -> int:
        result = t if (t := node["total"]) < 100000 else 0

        for v in node["children"].values():
            result += self._part_a_sol(v)

        return result

    def part_b(self):
        need = 30000000 - (70000000 - self.root["total"])
        print(f"need space: {need}")
        return self._part_b_sol(self.root, need)

    def _part_b_sol(self, node, goal) -> int:
        best = t if (t := node["total"]) >= goal else None

        for v in node["children"].values():
            if (_best := self._part_b_sol(v, goal)) and (not best or _best < best):
                best = _best

        return best


def test_simple():
    solution = Solution(Input(1))
    assert solution.part_a() == 95437
    assert solution.part_b() == 24933642


def test_challenge():
    solution = Solution(Input())
    assert solution.part_a() == 1845346
    assert solution.part_b() == 3636703
