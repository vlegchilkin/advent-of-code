import collections
from enum import Enum
from numbers import Complex
from typing import Iterable, Callable, Iterator, Optional
import numpy as np


class C(complex, Enum):
    NORTH = -1
    NORTH_EAST = -1 + 1j
    EAST = 1j
    SOUTH_EAST = 1 + 1j
    SOUTH = 1
    SOUTH_WEST = 1 - 1j
    WEST = -1j
    NORTH_WEST = -1 - 1j


C_DIAGONALS = (C.NORTH_EAST, C.SOUTH_EAST, C.SOUTH_WEST, C.NORTH_WEST)
C_BORDERS = (C.NORTH, C.SOUTH, C.WEST, C.EAST)
C_ALL = tuple(C)

C_TURNS = {
    C.EAST: {"R": C.SOUTH, "L": C.NORTH},
    C.SOUTH: {"R": C.WEST, "L": C.EAST},
    C.WEST: {"R": C.NORTH, "L": C.SOUTH},
    C.NORTH: {"R": C.EAST, "L": C.WEST},
}

C_OPPOSITE = {C.EAST: C.WEST, C.WEST: C.EAST, C.NORTH: C.SOUTH, C.SOUTH: C.NORTH}

C_MOVES = {
    "<": C.WEST,
    ">": C.EAST,
    "^": C.NORTH,
    "v": C.SOUTH,
}


class Spacer:
    def __init__(self, shape, *, directions: Iterable[Complex] = C_ALL):
        self.n = shape[0]
        self.m = shape[1]
        self.at = collections.defaultdict(lambda: 0)
        self.directions = C_ALL if directions is None else directions

    @staticmethod
    def build(arr: np.ndarray, *, directions: Iterable[Complex] = C_ALL) -> "Spacer":
        s = Spacer(arr.shape, directions=directions)
        for pos, v in np.ndenumerate(arr):
            s.at[complex(*pos)] = v
        return s

    def __iter__(self):
        yield from self.at.items()

    def links(
        self, pos, directions: Iterable[complex] = None, *, has_path: Callable[[complex], bool] = lambda x: True
    ) -> Iterator[complex]:

        for direct in directions or self.directions:
            to_pos = pos + direct
            if 0 <= to_pos.real < self.n and 0 <= to_pos.imag < self.m and has_path(to_pos):
                yield to_pos

    def bfs(
        self,
        pos,
        has_path: Callable[[complex], bool] = lambda x: True,
        test: Callable[[complex], bool] = None,
    ) -> (dict[complex, tuple[int, complex]], Optional[complex]):
        q = collections.deque([pos])
        visited = {pos: (0, None)}
        while q:
            p = q.popleft()
            for link in self.links(p, has_path=lambda x: has_path(x) and x not in visited):
                visited[link] = (visited[p][0] + 1, p)
                q.append(link)
                if test and test(link):
                    return visited, link
        return visited, None


def split_to_steps(vector: Complex) -> tuple[Complex, int]:
    if vector == 0:
        return vector, 0

    m = int(max(abs(vector.real), abs(vector.imag)))
    return vector / m, m
