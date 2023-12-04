import re

import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2023Day4(Solution):
    """2023/4: Scratchcards"""

    def __init__(self, inp: Input):
        data = inp.get_lines(lambda s: s.split(":")[1].split("|"))
        self.cards = [[set(map(int, re.findall(r"\d+", side))) for side in card] for card in data]

    @staticmethod
    def _score(card):
        left, right = card
        return sum([1 for num in right if num in left])

    def part_a(self):
        scores = list(map(self._score, self.cards))
        return sum([1 << (s - 1) for s in scores if s > 0])

    def part_b(self):
        total = [1] * len(self.cards)
        for i, card in enumerate(self.cards):
            score = self._score(card)
            limit = min(i + score + 1, len(self.cards))
            for j in range(i + 1, limit):
                total[j] += total[i]
        return sum(total)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2023Day4)
