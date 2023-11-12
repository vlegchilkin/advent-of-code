import collections
import re

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.tpl import t_sum, t_dist


class Year2017Day20(Solution):
    """2017/20: Particle Swarm"""

    def __init__(self, inp: Input):
        def parse(line):
            data = list(map(int, re.findall(r"-?\d+", line)))
            return tuple(data[:3]), tuple(data[3:6]), tuple(data[6:])

        self.particles = inp.get_lines(parse)

    def run(self, handler, moves=400):
        state = self.particles.copy()

        def move(p, v, a):
            v = t_sum(v, a)
            return t_sum(p, v), v, a

        for _ in range(moves):
            state = [move(*particle) for particle in state]
            handler(state)

    def part_a(self):
        best = None

        def handler(state):
            nonlocal best
            distances = [(t_dist(p, (0, 0, 0)), i) for i, (p, _, _) in enumerate(state)]
            best = min(distances)[1]

        self.run(handler)
        return best

    def part_b(self):
        alive = {i for i in range(len(self.particles))}

        def handler(state):
            nonlocal alive
            collide = collections.defaultdict(int)
            for index, (p, _, _) in enumerate(state):
                if index in alive:
                    collide[p] += 1
            alive = {index for index in alive if collide[state[index][0]] == 1}

        self.run(handler)
        return len(alive)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day20)
