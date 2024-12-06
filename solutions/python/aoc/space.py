import collections
import copy
from collections.abc import Mapping
from enum import Enum
from itertools import product
from typing import Iterable, Callable, Iterator, Optional, Generator, Union, TypeAlias, Any

import networkx as nx
import numpy as np
from numpy import inf

from aoc import math
from aoc.tpl import t_minmax


class C(complex, Enum):
    NORTH = -1 + 0j
    NORTH_EAST = -1 + 1j
    EAST = 0 + 1j
    SOUTH_EAST = 1 + 1j
    SOUTH = 1 + 0j
    SOUTH_WEST = 1 - 1j
    WEST = 0 - 1j
    NORTH_WEST = -1 - 1j


C_DIAGONALS = (C.NORTH_EAST, C.SOUTH_EAST, C.SOUTH_WEST, C.NORTH_WEST)
C_BORDERS = (C.NORTH, C.SOUTH, C.WEST, C.EAST)
C_ALL = tuple(C)

C_SIDES = {"U": C.NORTH, "D": C.SOUTH, "L": C.WEST, "R": C.EAST}
C_NSWE = {"N": C.NORTH, "S": C.SOUTH, "W": C.WEST, "E": C.EAST}

C_TURNS = {
    C.EAST: {"R": C.SOUTH, "L": C.NORTH, "F": C.EAST, "B": C.WEST},
    C.SOUTH: {"R": C.WEST, "L": C.EAST, "F": C.SOUTH, "B": C.NORTH},
    C.WEST: {"R": C.NORTH, "L": C.SOUTH, "F": C.WEST, "B": C.EAST},
    C.NORTH: {"R": C.EAST, "L": C.WEST, "F": C.NORTH, "B": C.SOUTH},
}

C_OPPOSITE = {c: C_TURNS[c]["B"] for c in C_TURNS}

C_MOVES = {"<": C.WEST, ">": C.EAST, "^": C.NORTH, "v": C.SOUTH}

ItFunc: TypeAlias = Callable[[int, int, int, int], Iterable[complex]]


class IT:
    TOP_LR: ItFunc = lambda n_, _n, m_, _m: [complex(n_, x) for x in range(m_, _m)]
    TOP_RL: ItFunc = lambda n_, _n, m_, _m: [complex(n_, _m - x - 1) for x in range(m_, _m)]

    BOTTOM_LR: ItFunc = lambda n_, _n, m_, _m: [complex(_n - 1, x) for x in range(m_, _m)]
    BOTTOM_RL: ItFunc = lambda n_, _n, m_, _m: [complex(_n - 1, _m - x - 1) for x in range(m_, _m)]

    LEFT_TB: ItFunc = lambda n_, _n, m_, _m: [complex(x, m_) for x in range(n_, _n)]
    LEFT_BT: ItFunc = lambda n_, _n, m_, _m: [complex(_n - x - 1, m_) for x in range(n_, _n)]

    RIGHT_TB: ItFunc = lambda n_, _n, m_, _m: [complex(x, _m - 1) for x in range(n_, _n)]
    RIGHT_BT: ItFunc = lambda n_, _n, m_, _m: [complex(_n - x - 1, _m - 1) for x in range(n_, _n)]

    CORNERS: ItFunc = lambda n_, _n, m_, _m: [
        complex(n_, m_),
        complex(n_, _m - 1),
        complex(_n - 1, _m - 1),
        complex(_n - 1, m_),
    ]


class Spacer(Mapping):
    def __init__(self, shape=None, *, ranges=0, at=None, directions: Iterable[complex] = C_ALL):
        if ranges is None:
            self.ranges = ((-inf, inf), (-inf, inf))
        else:
            self.ranges = ranges or ((0, shape[0]), (0, shape[1]))
        self.at = at or dict()
        self.directions = C_ALL if directions is None else directions

    @staticmethod
    def build(
        data: Union[np.ndarray, dict[tuple[int, int], Any]], *, ranges=0, directions: Iterable[complex] = C_ALL
    ) -> "Spacer":
        if type(data) == dict:
            return Spacer._build_from_dict(data, ranges, directions)
        elif type(data) == np.ndarray:
            return Spacer._build_from_array(data, ranges, directions)
        else:
            raise ValueError("Non-supported data object")

    @staticmethod
    def _build_from_dict(data: dict[tuple[int, int], Any], ranges, directions) -> "Spacer":
        if ranges == 0:
            mm = t_minmax(list(data.keys()))
            ranges = (mm[0], (mm[1][0] + 1, mm[1][1] + 1))
        s = Spacer(ranges=ranges, directions=directions)
        for pos, v in data.items():
            if v is not None:
                s.at[complex(*pos)] = v
        return s

    @staticmethod
    def _build_from_array(arr: np.ndarray, ranges, directions) -> "Spacer":
        s = Spacer(arr.shape, ranges=ranges, directions=directions)
        for pos, v in np.ndenumerate(arr):
            if v is not None:
                _pos = pos[0] * 1j if len(pos) == 1 else complex(*pos)
                s.at[_pos] = v
        return s

    def __copy__(self):
        return Spacer(ranges=self.ranges, at=self.at, directions=self.directions)

    def __deepcopy__(self, memo):
        return Spacer(ranges=self.ranges, at=copy.deepcopy(self.at, memo), directions=copy.deepcopy(self.directions))

    def __getitem__(self, __k: complex) -> Any:
        return self.at[__k]

    def __setitem__(self, __k: complex, value: Any):
        self.at[__k] = value

    def __delitem__(self, __k: complex):
        del self.at[__k]

    def __len__(self) -> int:
        return len(self.at)

    def __iter__(self):
        yield from self.at.items()

    def __contains__(self, key):
        return key in self.at

    @property
    def shape(self):
        return self.n, self.m

    @property
    def n(self):
        return self.ranges[0][1]

    @property
    def m(self):
        return self.ranges[1][1]

    def transform(self, func: Callable):
        result = Spacer(ranges=self.ranges, directions=self.directions)
        for pos, value in self:
            if (new_value := func(pos, value)) is not None:
                result[pos] = new_value

        return result

    def to_digraph(self, weight: Callable[[complex, complex], int] = lambda src, dst: 1):
        graph = nx.DiGraph()
        for pos in self.at:
            graph.add_node(pos)

        graph.add_weighted_edges_from(self.edges(weight=weight))
        return graph

    def edges(
        self,
        weight: Callable[[complex, complex], int] = lambda src, dst: 1,
        *,
        directions: Iterable[complex] = None,
    ) -> Generator[tuple[complex, complex, int], None, None]:
        for pos, _ in self:
            for link in self.links(pos, directions):
                if (w := weight(self.at[pos], self.at[link])) is not None:
                    yield pos, link, w

    def links(
        self,
        pos,
        directions: Iterable[complex] = None,
        has_path: Callable[[complex], bool] = None,
    ) -> Iterator[complex]:
        has_path = has_path or (lambda p: p in self)
        for direct in directions or self.directions:
            to_pos = pos + direct
            if (
                self.ranges[0][0] <= to_pos.real < self.ranges[0][1]
                and self.ranges[1][0] <= to_pos.imag < self.ranges[1][1]
                and has_path(to_pos)
            ):
                yield to_pos

    def bfs(
        self,
        pos,
        has_path: Callable[[complex], bool] = None,
        test: Callable[[complex], bool] = None,
    ) -> (dict[complex, tuple[int, complex]], Optional[complex]):
        has_path = has_path or (lambda x: x in self)
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

    def is_inside_ranges(self, pos: complex) -> bool:
        return self.ranges[0][0] <= pos.real < self.ranges[0][1] and self.ranges[1][0] <= pos.imag < self.ranges[1][1]

    def move(self, pos: complex, direction: C, *, cyclic=True, has_path: Callable[[complex], bool] = None):
        if not self.is_inside_ranges(_pos := pos + direction):
            if not cyclic:
                return None

            x = _pos.real % self.n
            if x < 0:
                x += self.n

            y = _pos.imag % self.m
            if y < 0:
                y += self.m

            _pos = complex(x, y)

        if (has_path or (lambda p: p in self))(_pos):
            return _pos

    def iter(self, test: Callable[[complex], bool] = None, *, it: Optional[ItFunc] = None) -> Iterator[complex]:
        def full_iter():
            for i, j in product(range(self.n), range(self.m)):
                if not test or test(complex(i, j)):
                    yield complex(i, j)

        def it_func_iter():
            for pos in it(*self.ranges[0], *self.ranges[1]):
                if test and not test(pos):
                    continue
                yield pos

        return full_iter() if it is None else it_func_iter()

    def to_array(self, swap_xy=False):
        return to_array(self.at, swap_xy)

    def __str__(self) -> str:
        return to_str(self.at, ranges=self.ranges)

    def minmax(self) -> (complex, complex):
        return minmax(self.at)

    def find_ranges(self) -> (tuple[int, int], tuple[int, int]):
        return ranges(self.at)

    def rotate(self, count, row=None, col=None):
        if row is not None and col is None:
            vect = C.EAST * (count % self.m)

            def it():
                return (complex(row, j) for j in range(self.m))

        elif row is None and col is not None:
            vect = C.SOUTH * (count % self.n)

            def it():
                return (complex(i, col) for i in range(self.n))

        else:
            raise ValueError("Only one of the {row,col} should be non-None value")

        subs = {}
        for pos in it():
            if pos in self:
                subs[self.move(pos, vect, has_path=lambda _: True)] = self[pos]
                del self[pos]
        self.at.update(subs)


def split_to_steps(vector: complex) -> tuple[complex, int]:
    if vector == 0:
        return vector, 0

    m = int(max(abs(vector.real), abs(vector.imag)))
    return vector / m, m


def minmax(points: Iterable[complex]) -> (complex, complex):
    reals, imags = [point.real for point in points], [point.imag for point in points]
    return complex(min(reals), min(imags)), complex(max(reals), max(imags))


def ranges(points: Iterable[complex]) -> (tuple[int, int], tuple[int, int]):
    reals, imags = [int(point.real) for point in points], [int(point.imag) for point in points]
    return (min(reals), max(reals) + 1), (min(imags), max(imags) + 1)


def to_array(points: Union[dict, set], swap_xy=False, ranges=None) -> np.ndarray:
    _min, _max = (
        minmax(points)
        if ranges is None or inf in [ranges[0][1], ranges[1][1]]
        else (complex(ranges[0][0], ranges[1][0]), complex(ranges[0][1] - 1, ranges[1][1] - 1))
    )

    def get_x(c):
        return int(c.imag if swap_xy else c.real)

    def get_y(c):
        return int(c.real if swap_xy else c.imag)

    ar = np.full((get_x(_max - _min) + 1, get_y(_max - _min) + 1), fill_value=".", dtype=object)
    for point in points:
        ar[get_x(point - _min), get_y(point - _min)] = 1 if type(points) == set else points[point]
    return ar


def to_str(points: Union[dict, set], swap_xy=False, ranges=None) -> str:
    ar = to_array(points, swap_xy, ranges)
    result = ""
    for row in ar:
        for col in row:
            result += str(col)
        result += "\n"
    return result


def to_t(point: complex) -> tuple[int, int]:
    return int(point.real), int(point.imag)


def c_delta(x: complex, y: complex):
    return complex(abs(x.real - y.real), abs(x.imag - y.imag))


def c_dist(x: complex, y: complex, *, manhattan: bool = True) -> Union[int, float]:
    if manhattan:
        delta = c_delta(x, y)
        return int(delta.real + delta.imag)
    else:
        return math.dist((x.real, x.imag), (y.real, y.imag))
