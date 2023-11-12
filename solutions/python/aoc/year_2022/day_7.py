from dataclasses import dataclass, field
from typing import Callable, Any

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


@dataclass
class Dir:
    parent: "Dir" = None
    dirs: dict[str, "Dir"] = field(default_factory=lambda: dict())
    files: dict[str, int] = field(default_factory=lambda: dict())

    def resolve(self, name):
        if name == "..":
            return self.parent
        if name not in self.dirs:
            self.dirs[name] = Dir(parent=self)
        return self.dirs[name]

    def total(self, callback: Callable[[int], Any] = None) -> int:
        size = sum(self.files.values()) + sum([d.total(callback) for d in self.dirs.values()])
        if callback:
            callback(size)
        return size

    @staticmethod
    def build_fs(input_iter) -> "Dir":
        def ls():
            nonlocal line
            while (line := next(input_iter, None)) and not line.startswith("$"):
                desc, name = line.split(" ")
                if desc == "dir":
                    if name not in node.dirs:
                        node.dirs[name] = Dir(parent=node)
                else:
                    node.files[name] = int(desc)

        def cd():
            nonlocal node, line
            node = node.resolve(line[5:])
            line = next(input_iter, None)

        genesis = node = Dir()
        line = next(input_iter)
        while line:
            if line.startswith("$ cd"):
                cd()
            elif line.startswith("$ ls"):
                ls()
            else:
                raise ValueError(f"Wrong Input: {line}")
        return genesis


class Year2022Day7(Solution):
    def __init__(self, inp: Input):
        self.fs = Dir.build_fs(inp.get_iter())

    def part_a(self):
        total_size = 0

        def callback(size):
            nonlocal total_size
            total_size += size if size < 100000 else 0

        self.fs.total(callback)
        return total_size

    def part_b(self):
        need_space = 30000000 - (70000000 - self.fs.total())
        best_size = None

        def callback(size):
            nonlocal best_size
            if need_space <= size and (best_size is None or size < best_size):
                best_size = size

        self.fs.total(callback)

        return best_size


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2022Day7)
