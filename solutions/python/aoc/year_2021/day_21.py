import collections
import itertools
from functools import cache

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.tpl import t_sum


class Year2021Day21(Solution):
    def __init__(self, inp: Input):
        self.positions = [p.pos for p in inp.get_objects("Player {{id|to_int}} starting position: {{pos|to_int}}")]

    def part_a(self):
        dice, rolled = itertools.cycle(range(1, 101)), 0
        scores = collections.defaultdict(lambda: 0)
        positions, turn = self.positions.copy(), 0
        while scores[1 - turn] < 1000:
            steps = sum(next(dice) for _ in range(3))
            rolled += 3
            positions[turn] = (positions[turn] + steps - 1) % 10 + 1
            scores[turn] += positions[turn]
            turn = 1 - turn

        return scores[turn] * rolled

    def part_b(self):
        @cache
        def recu(s, p, turn, step, t3):
            score = (0, 0)
            for d in range(1, 4):
                _t3 = t3 + d
                if step < 2:
                    v_score = recu(s, p, turn, step + 1, _t3)
                else:
                    pos = (p[turn] + _t3 - 1) % 10 + 1
                    _s = (s[0], s[1] + pos) if turn else (s[0] + pos, s[1])
                    if _s[turn] >= 21:
                        v_score = (0, 1) if turn else (1, 0)
                    else:
                        _p = (p[0], pos) if turn else (pos, p[1])
                        v_score = recu(_s, _p, 1 - turn, 0, 0)
                score = t_sum(score, v_score)
            return score

        return max(recu((0, 0), (self.positions[0], self.positions[1]), 0, 0, 0))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2021Day21)
