from dataclasses import dataclass, field
from typing import Callable, Any

import pytest

from aoc import Input, get_puzzles, PuzzleData


@dataclass
class Dir:
    parent: "Dir" = None
    sub_dirs: dict[str, "Dir"] = field(default_factory=lambda: dict())
    files: dict[str, int] = field(default_factory=lambda: dict())

    def resolve(self, name):
        if name == "..":
            return self.parent
        if name not in self.sub_dirs:
            self.sub_dirs[name] = Dir(parent=self)
        return self.sub_dirs[name]

    def total(self, callback: Callable[[int], Any] = None) -> int:
        size = sum(self.files.values()) + sum([d.total(callback) for d in self.sub_dirs.values()])
        if callback:
            callback(size)
        return size

    @staticmethod
    def build_fs(input_iter) -> "Dir":
        genesis = node = Dir()
        line = next(input_iter)
        while line:
            if line.startswith("$ cd"):
                node = node.resolve(line[5:])
                line = next(input_iter, None)
            elif line.startswith("$ ls"):
                while (line := next(input_iter, None)) and not line.startswith("$"):
                    if not line.startswith("dir "):
                        size, name = line.split(" ")
                        node.files[name] = int(size)
            else:
                raise ValueError(f"Wrong Input: {line}")
        return genesis


class Solution:
    def __init__(self, inp: Input):
        self.fs = Dir.build_fs(inp.get_iter())

    def part_a(self):
        total_size = 0

        def callback(dir_size):
            nonlocal total_size
            total_size += dir_size if dir_size < 100000 else 0

        self.fs.total(callback)
        return total_size

    def part_b(self):
        need_space = 30000000 - (70000000 - self.fs.total())
        best = None

        def callback(dir_size):
            nonlocal best
            if need_space <= dir_size and (best is None or dir_size < best):
                best = dir_size

        self.fs.total(callback)

        return best


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
