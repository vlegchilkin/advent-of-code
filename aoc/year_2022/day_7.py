from dataclasses import dataclass, field

import pytest

from aoc import Input, get_puzzles, PuzzleData


@dataclass
class Node:
    parent: "Node" = None
    children: dict[str, "Node"] = field(default_factory=lambda: dict())
    files_size: int = 0
    total: int = 0


class Solution:
    def __init__(self, inp: Input):
        input_iter = inp.get_iter()
        self.root = node = Node()

        line = next(input_iter)
        while line:
            if line.startswith("$ cd"):
                node = self._cd(line, node)
                line = next(input_iter, None)
            elif line.startswith("$ ls"):
                line = self._ls(input_iter, node)
            else:
                raise ValueError(f"Wrong Input: {line}")

        self._count_total(self.root)

    @staticmethod
    def _ls(input_iter, node):
        while (line := next(input_iter, None)) and not line.startswith("$"):
            if not line.startswith("dir "):
                size, _ = line.split(" ")
                node.files_size += int(size)
        return line

    @staticmethod
    def _cd(line, node):
        if (name := line[5:]) == "..":
            return node.parent

        if name not in node.children:
            node.children[name] = Node(parent=node)

        return node.children[name]

    def _count_total(self, node: Node) -> int:
        result = node.files_size

        for child_node in node.children.values():
            result += self._count_total(child_node)

        node.total = result
        return result

    def part_a(self):
        return self._part_a_sol(self.root)

    def _part_a_sol(self, node: Node) -> int:
        result = t if (t := node.total) < 100000 else 0

        for v in node.children.values():
            result += self._part_a_sol(v)

        return result

    def part_b(self):
        need_space = 30000000 - (70000000 - self.root.total)
        return self._part_b_sol(self.root, need_space)

    def _part_b_sol(self, node: Node, goal) -> int:
        best = t if (t := node.total) >= goal else None

        for v in node.children.values():
            if (_best := self._part_b_sol(v, goal)) and (not best or _best < best):
                best = _best

        return best


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
